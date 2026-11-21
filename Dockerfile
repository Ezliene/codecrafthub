# Start from a small official Python image
FROM python:3.12-slim

# All following commands run inside /app
WORKDIR /app

# Install dependencies first (Docker caches this step, so rebuilds are fast)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app.py .

# Settings for running inside a container
ENV HOST=0.0.0.0 \
    FLASK_DEBUG=0 \
    DATA_FILE=/data/courses.json

# Folder where courses.json will live (we mount a volume here)
RUN mkdir /data

# Document the port the app listens on
EXPOSE 5000

# Start the API
CMD ["python", "app.py"]
