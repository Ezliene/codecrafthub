# CodeCraftHub 🚀

A simple REST API for tracking the courses you want to learn. Built with **Python + Flask**, storing data in a plain **JSON file** (no database needed).

This project is made for beginners learning REST APIs for the first time.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Installation](#3-installation)
4. [Running the Application](#4-running-the-application)
5. [API Documentation](#5-api-documentation)
6. [Testing](#6-testing)
7. [Troubleshooting](#7-troubleshooting)
8. [Project Structure](#8-project-structure)

---

## 1. Project Overview

CodeCraftHub lets developers keep a list of courses they want to learn. For each course you can store:

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique number, generated automatically (starts at 1) | `1` |
| `name` | Course name (required) | `"Flask Basics"` |
| `description` | What the course is about (required) | `"Learn routes and JSON"` |
| `target_date` | When you want to finish, format `YYYY-MM-DD` (required) | `"2026-12-31"` |
| `status` | `Not Started`, `In Progress`, or `Completed` (required) | `"In Progress"` |
| `created_at` | Timestamp, generated automatically | `"2026-11-20T14:30:00"` |

### What is a REST API? (quick explanation)

A REST API is a program that waits for **requests** over HTTP and sends back **responses** (usually JSON). Each request has:

- A **method** that says what you want to do: `GET` (read), `POST` (create), `PUT` (update), `DELETE` (remove)
- A **URL** that says what you want to do it to, like `/api/courses/1`

Together these four methods are called **CRUD**: Create, Read, Update, Delete. CodeCraftHub does all four.

---

## 2. Features

- ✅ Add, list, view, update, and delete courses (full CRUD)
- ✅ Data saved in `courses.json`, which is created automatically
- ✅ Auto-generated IDs and timestamps
- ✅ Input validation (required fields, valid status, valid date)
- ✅ Clear JSON error messages with correct HTTP status codes
- ✅ Safe file writing and handling of file read/write errors
- ✅ No login or user accounts, so you can focus on REST basics

---

## 3. Installation

### What you need

- **Python 3.8 or newer**. Check with: `python --version`
- **VS Code** (or any code editor)

### Step by step

**Step 1: Create a project folder** called `codecrafthub` and put `app.py` inside it.

**Step 2: Open the folder in VS Code** (`File → Open Folder…`).

**Step 3: Open the terminal** in VS Code (`Terminal → New Terminal`).

**Step 4 (optional but recommended): Create a virtual environment.** This keeps this project's packages separate from the rest of your computer.

```bash
python -m venv venv
```

Activate it:

| System | Command |
|--------|---------|
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| Mac / Linux / Git Bash | `source venv/bin/activate` |

You'll see `(venv)` at the start of your terminal line when it's active.

> If PowerShell says scripts are disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again. Or just skip this step.

**Step 5: Install Flask**

```bash
pip install flask
```

*(Optional)* To record the dependency, create a file called `requirements.txt` containing the single line `flask`. Anyone can then install it with `pip install -r requirements.txt`.

---

## 4. Running the Application

In the terminal, from inside the project folder:

```bash
python app.py
```

(On Mac/Linux you may need `python3 app.py`.)

You should see:

```
* Running on http://127.0.0.1:5000
```

🎉 Your API is live! `courses.json` is created automatically if it doesn't exist.

- **Leave this terminal open.** Closing it stops the server.
- **Stop the server** with `Ctrl + C`.
- Quick check: open <http://127.0.0.1:5000/api/courses> in your browser. You should see `[]`.

---

## 5. API Documentation

**Base URL:** `http://127.0.0.1:5000`

### Endpoints at a glance

| Method | Endpoint | What it does | Success code |
|--------|----------|--------------|--------------|
| `POST` | `/api/courses` | Add a new course | `201 Created` |
| `GET` | `/api/courses` | Get all courses | `200 OK` |
| `GET` | `/api/courses/<id>` | Get one course | `200 OK` |
| `PUT` | `/api/courses/<id>` | Update a course | `200 OK` |
| `DELETE` | `/api/courses/<id>` | Delete a course | `200 OK` |

> **How to read the examples:** each example is shown for **PowerShell** (Windows) and **curl** (Mac, Linux, Git Bash). Use the one that matches your terminal.

---

### 5.1 Add a course: `POST /api/courses`

All four fields are required.

**Request body:**

```json
{
  "name": "Flask Basics",
  "description": "Learn routes and JSON responses",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

**PowerShell:**

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/courses -ContentType "application/json" -Body '{"name":"Flask Basics","description":"Learn routes and JSON responses","target_date":"2026-12-31","status":"Not Started"}'
```

**curl:**

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d '{"name":"Flask Basics","description":"Learn routes and JSON responses","target_date":"2026-12-31","status":"Not Started"}'
```

**Response: `201 Created`**

```json
{
  "id": 1,
  "name": "Flask Basics",
  "description": "Learn routes and JSON responses",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-11-20T14:30:00"
}
```

---

### 5.2 Get all courses: `GET /api/courses`

**PowerShell:**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/courses
```

**curl:**

```bash
curl -i http://127.0.0.1:5000/api/courses
```

**Response: `200 OK`**: a list (empty `[]` if there are no courses)

```json
[
  {
    "id": 1,
    "name": "Flask Basics",
    "description": "Learn routes and JSON responses",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-11-20T14:30:00"
  }
]
```

---

### 5.3 Get one course: `GET /api/courses/<id>`

**PowerShell:**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/courses/1
```

**curl:**

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

**Response: `200 OK`**: the single course object. If the ID doesn't exist you get a `404` (see error table below).

---

### 5.4 Update a course: `PUT /api/courses/<id>`

Send **only the fields you want to change**. `id` and `created_at` can't be changed.

**Request body (example: change only the status):**

```json
{
  "status": "In Progress"
}
```

**PowerShell:**

```powershell
Invoke-RestMethod -Method Put -Uri http://127.0.0.1:5000/api/courses/1 -ContentType "application/json" -Body '{"status":"In Progress"}'
```

**curl:**

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 -H "Content-Type: application/json" -d '{"status":"In Progress"}'
```

**Response: `200 OK`**: the full updated course.

---

### 5.5 Delete a course: `DELETE /api/courses/<id>`

**PowerShell:**

```powershell
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:5000/api/courses/1
```

**curl:**

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

**Response: `200 OK`**

```json
{
  "message": "Course 1 deleted successfully."
}
```

---

### 5.6 Error responses

Every error comes back as JSON with an `error` message:

```json
{
  "error": "Course with id 999 not found."
}
```

| Status code | Meaning | Example cause |
|-------------|---------|---------------|
| `400 Bad Request` | You sent something invalid | Missing field, bad status, bad date, body isn't valid JSON |
| `404 Not Found` | Thing doesn't exist | Course ID not found, or unknown URL |
| `405 Method Not Allowed` | Right URL, wrong method | `DELETE /api/courses` (no ID) |
| `500 Internal Server Error` | Problem on the server | `courses.json` can't be read or is corrupted |

### 5.7 Validation rules

- `name`, `description`: required, must be non-empty text
- `target_date`: must be a real date written as `YYYY-MM-DD` (e.g. `2026-12-31`; `2026-02-30` is rejected)
- `status`: must be exactly `Not Started`, `In Progress`, or `Completed` (capitalization matters)

---

## 6. Testing

Test by hand, with the server running in one terminal and your commands in a **second terminal** (click the `+` in VS Code's terminal panel).

### Quick test (5 minutes)

Run these in order:

1. **List (empty):** `GET /api/courses` → expect `[]`
2. **Add a course:** `POST` the example from 5.1 → expect `201` and `"id": 1`
3. **List again:** expect your course in the list
4. **Get one:** `GET /api/courses/1` → expect the course
5. **Update:** `PUT /api/courses/1` with `{"status":"In Progress"}` → expect the status changed
6. **Delete:** `DELETE /api/courses/1` → expect the success message
7. **Confirm:** `GET /api/courses` → expect `[]` again

### Error tests to try

| Test | What to send | Expected |
|------|--------------|----------|
| Missing fields | `POST` with `{"name":"Only a name"}` | `400` |
| Bad status | `POST` with `"status":"Done"` | `400` |
| Bad date | `POST` with `"target_date":"31-12-2026"` | `400` |
| Not found | `GET /api/courses/999` | `404` |
| Wrong method | `DELETE /api/courses` | `405` |

### Tools you can use

- **Browser:** good for `GET` requests only (just paste the URL)
- **PowerShell / curl:** the commands in section 5
- **Thunder Client:** a VS Code extension with a friendly point-and-click interface, great for beginners
- **Postman:** a free app for testing APIs

---

## 7. Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `python is not recognized` | Python isn't installed or not on PATH | Reinstall Python and tick **"Add Python to PATH"**. Or try `py app.py` / `python3 app.py` |
| `No module named flask` | Flask isn't installed (or venv not active) | Run `pip install flask`. If you use a venv, activate it first |
| `Address already in use` / port 5000 busy | Another program (or an old server) is using port 5000 | Stop the old server with `Ctrl + C`, or change the port: `app.run(debug=True, port=5001)` |
| `curl -i` asks for `Uri:` in PowerShell | In PowerShell, `curl` is an alias for another command | Use `curl.exe`, or use the `Invoke-RestMethod` examples |
| JSON errors when using curl in PowerShell | PowerShell mangles quotes | Use the `Invoke-RestMethod` examples, or use Git Bash |
| `400` with "Request body must be valid JSON object" | Bad JSON or missing `Content-Type` header | Check commas and quotes. Make sure you send `Content-Type: application/json` |
| `404` on a URL that looks right | Typo, or ID doesn't exist | Check the URL starts with `/api/courses`. IDs must be numbers |
| `500` "courses.json is corrupted" | The file contains invalid JSON | Open `courses.json`, replace everything with `[]`, save. (Or delete the file. It's recreated automatically) |
| Changes to `app.py` don't show up | Server wasn't restarted | Stop with `Ctrl + C` and run `python app.py` again. (Debug mode usually auto-reloads) |
| Browser shows nothing / can't connect | Server isn't running | Check the first terminal shows `Running on http://127.0.0.1:5000` |

---

## 8. Project Structure

```
codecrafthub/
├── app.py            # The whole application: routes, validation, file handling
├── courses.json      # Your data. Created automatically on first run
├── requirements.txt  # (optional) Python dependencies: just "flask"
└── README.md         # This file
```

### How `app.py` is organized

| Section | What it does |
|---------|--------------|
| **Settings** | File path, allowed statuses, required fields |
| **File helpers** (`load_courses`, `save_courses`, `init_data_file`) | Read and write `courses.json` |
| **Data helpers** (`get_next_id`, `find_course`) | Generate IDs, look up a course |
| **Validation** (`validate_fields`) | Checks incoming data and returns an error message if invalid |
| **Routes** | The five endpoints (POST, GET all, GET one, PUT, DELETE) |
| **Error handlers** | Make sure all errors come back as JSON |

### How a request flows through the app

Every endpoint follows the same pattern:

1. **Receive** the request (read the JSON body, if any)
2. **Validate** the data → return `400` if it's wrong
3. **Load** courses from `courses.json`
4. **Change** the list in Python (add, update, or remove)
5. **Save** the list back to `courses.json`
6. **Respond** with JSON and a status code

---

## Known Limitations (by design)

This is a learning project, so some things are intentionally simple:

- **JSON file, not a database.** If two requests write at the exact same moment, one could be lost. Fine for learning, not for production.
- **No authentication.** Anyone who can reach the server can change the data.
- **Debug mode is on.** Never run with `debug=True` on a public server.

## Ideas for Next Steps 💡

- Filter courses by status (`GET /api/courses?status=Completed`)
- Sort by `target_date`
- Add a simple HTML page that talks to the API
- Swap the JSON file for SQLite
- Write automated tests with `pytest`

Happy learning! 🎓
