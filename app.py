"""
CodeCraftHub - a simple REST API for tracking courses you want to learn.

Stack: Python + Flask, with a JSON file (courses.json) as the "database".
No authentication, no real database. This project is for learning REST basics.

Run it:
    pip install flask
    python app.py
Then open: http://127.0.0.1:5000/api/courses
"""

import json
import os
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

# Build the path from this file's location, so courses.json is always found
# no matter which folder you run the app from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_FILE env var lets Docker point this at a mounted folder; default is next to app.py.
DATA_FILE = os.environ.get("DATA_FILE", os.path.join(BASE_DIR, "courses.json"))

# The only values allowed for "status"
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]

# Fields the client must send when creating a course
REQUIRED_FIELDS = ["name", "description", "target_date", "status"]


# ---------------------------------------------------------------------------
# Custom error for file problems
# ---------------------------------------------------------------------------

class StorageError(Exception):
    """Raised when we can't read from or write to courses.json."""


# ---------------------------------------------------------------------------
# Helper functions: reading and writing the JSON file
# ---------------------------------------------------------------------------

def init_data_file():
    """Create courses.json (with an empty list) if it doesn't exist yet."""
    if not os.path.exists(DATA_FILE):
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # make sure the folder exists
            with open(DATA_FILE, "w") as f:
                json.dump([], f)
        except OSError as e:
            raise StorageError(f"Could not create {DATA_FILE}: {e}")


def load_courses():
    """Read all courses from the JSON file and return them as a Python list."""
    init_data_file()  # makes sure the file exists before we read it
    try:
        with open(DATA_FILE, "r") as f:
            courses = json.load(f)
    except json.JSONDecodeError:
        # File exists but contains broken JSON. We raise an error instead of
        # returning [] so we never silently overwrite your data.
        raise StorageError("courses.json is corrupted (invalid JSON).")
    except OSError as e:
        raise StorageError(f"Could not read courses.json: {e}")

    if not isinstance(courses, list):
        raise StorageError("courses.json must contain a list of courses.")
    return courses


def save_courses(courses):
    """Write the full list of courses back to the JSON file."""
    # Safe-write trick: write to a temp file first, then swap it in.
    # If something crashes mid-write, the original file stays intact.
    temp_file = DATA_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            json.dump(courses, f, indent=2)  # indent=2 keeps it readable
        os.replace(temp_file, DATA_FILE)
    except OSError as e:
        raise StorageError(f"Could not write to courses.json: {e}")


def get_next_id(courses):
    """Return the next ID: 1 for an empty list, otherwise highest ID + 1."""
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


def find_course(courses, course_id):
    """Return the course with this ID, or None if it doesn't exist."""
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


# ---------------------------------------------------------------------------
# Helper functions: validating incoming data
# ---------------------------------------------------------------------------

def validate_fields(data, require_all):
    """
    Check the data sent by the client.

    require_all=True  -> every required field must be present (used by POST)
    require_all=False -> only validate the fields that were sent (used by PUT)

    Returns an error message (string) if something is wrong, else None.
    """
    # Check for missing required fields
    if require_all:
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            return f"Missing required field(s): {', '.join(missing)}"

    # Check text fields: must be non-empty strings
    for field in ["name", "description"]:
        if field in data:
            value = data[field]
            if not isinstance(value, str) or not value.strip():
                return f"'{field}' must be a non-empty string."

    # Check the date format (YYYY-MM-DD)
    if "target_date" in data:
        value = data["target_date"]
        if not isinstance(value, str):
            return "'target_date' must be a string in YYYY-MM-DD format."
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return "'target_date' must be a valid date in YYYY-MM-DD format."

    # Check the status value
    if "status" in data and data["status"] not in VALID_STATUSES:
        return f"'status' must be one of: {', '.join(VALID_STATUSES)}"

    return None  # no problems found


def get_json_body():
    """
    Get the JSON body from the request.
    Returns None if the body is missing, not valid JSON, or not an object.
    """
    data = request.get_json(silent=True)  # silent=True -> None instead of crash
    if not isinstance(data, dict):
        return None
    return data


# ---------------------------------------------------------------------------
# Routes (the API endpoints)
# ---------------------------------------------------------------------------

@app.route("/api/courses", methods=["POST"])
def add_course():
    """POST /api/courses - add a new course."""
    data = get_json_body()
    if data is None:
        return jsonify({"error": "Request body must be valid JSON object."}), 400

    error = validate_fields(data, require_all=True)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()

    new_course = {
        "id": get_next_id(courses),                              # auto-generated
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.now().isoformat(timespec="seconds"),  # auto timestamp
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201  # 201 = Created


@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """GET /api/courses - return every course."""
    courses = load_courses()
    return jsonify(courses), 200


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """GET /api/courses/stats - return the total and a count per status."""
    courses = load_courses()

    # Start every status at 0 so they always appear, even with no courses
    by_status = {status: 0 for status in VALID_STATUSES}

    # Go through each course and add 1 to its status counter
    for course in courses:
        status = course.get("status")
        if status in by_status:
            by_status[status] += 1

    return jsonify({
        "total": len(courses),
        "by_status": by_status,
    }), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """GET /api/courses/<id> - return one course."""
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": f"Course with id {course_id} not found."}), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """PUT /api/courses/<id> - update a course (send only the fields to change)."""
    data = get_json_body()
    if data is None:
        return jsonify({"error": "Request body must be valid JSON object."}), 400

    # Only these fields can be changed. id and created_at are protected.
    updates = {key: data[key] for key in REQUIRED_FIELDS if key in data}
    if not updates:
        return jsonify({
            "error": f"Provide at least one field to update: {', '.join(REQUIRED_FIELDS)}"
        }), 400

    error = validate_fields(updates, require_all=False)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()
    course = find_course(courses, course_id)
    if course is None:
        return jsonify({"error": f"Course with id {course_id} not found."}), 404

    # Apply the changes (strip spaces from text fields)
    for key, value in updates.items():
        course[key] = value.strip() if key in ("name", "description") else value

    save_courses(courses)
    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """DELETE /api/courses/<id> - remove a course."""
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": f"Course with id {course_id} not found."}), 404

    courses.remove(course)
    save_courses(courses)

    return jsonify({"message": f"Course {course_id} deleted successfully."}), 200


# ---------------------------------------------------------------------------
# CORS: lets the HTML dashboard (served from another port, e.g. Live Server on
# 5500) call this API. Without these headers the browser blocks the requests.
# "*" means "any website may call me" - fine for learning, not for production.
# ---------------------------------------------------------------------------

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# ---------------------------------------------------------------------------
# Error handlers: make sure errors come back as JSON, not HTML pages
# ---------------------------------------------------------------------------

@app.errorhandler(StorageError)
def handle_storage_error(e):
    """Any file read/write problem ends up here."""
    return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def handle_not_found(e):
    """Unknown URL (e.g. /api/banana)."""
    return jsonify({"error": "Resource not found."}), 404


@app.errorhandler(405)
def handle_method_not_allowed(e):
    """Right URL, wrong method (e.g. DELETE /api/courses)."""
    return jsonify({"error": "Method not allowed for this endpoint."}), 405


@app.errorhandler(500)
def handle_server_error(e):
    """Anything unexpected."""
    return jsonify({"error": "Internal server error."}), 500


# ---------------------------------------------------------------------------
# Start the app
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_data_file()  # create courses.json on startup if it's missing
    # Defaults are for running on your own computer. Docker overrides them:
    #   HOST=0.0.0.0 -> accept connections from outside the container
    #   FLASK_DEBUG=0 -> debug mode off (never leave it on in a shared/public setup)
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host=host, debug=debug)
