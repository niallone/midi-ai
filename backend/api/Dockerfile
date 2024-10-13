# Use the official Python 3.10 slim image as a parent image
# This image is smaller than the full Python image, reducing the final image size
# Using 3.10 due to project requiring Tensorflow 2.12
FROM python:3.10-slim

# Set the working directory in the container
# All subsequent commands will be run from this directory
WORKDIR /usr/src/api

# Set environment variables
# These variables are used by Flask and our application

# Specifies the main application file
ENV FLASK_APP=app/api.py
# Allows connections from outside the container
ENV FLASK_RUN_HOST=0.0.0.0
# Sets the port on which the app will run
ENV FLASK_RUN_PORT=4050
 # Ensures Python output is sent straight to terminal (helpful for logging)
ENV PYTHONUNBUFFERED=1
# Adds the working directory to Python path
ENV PYTHONPATH=/usr/src/api:$PYTHONPATH
 # Sets the timeout for Hypercorn server (in seconds)
ENV HYPERCORN_TIMEOUT=300

# Update the package index and install system dependencies
# libsndfile1 is required for audio file processing
# Clean up the apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
# This is done before copying the rest of the app to leverage Docker cache
COPY requirements.txt .

# Copy the application code into the container
# The .dockerignore file should be used to exclude unnecessary files
COPY app/ app/

# Copy additional necessary files
COPY wsgi.py .
COPY conftest.py .

# Install Python dependencies
# --no-cache-dir option tells pip to not save the downloaded packages locally
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4050 available to the world outside this container
# This doesn't actually publish the port, it just documents which port should be published
EXPOSE 4050

# Run the application using Hypercorn when the container launches
# Hypercorn is an ASGI server that can run Flask applications
# --bind 0.0.0.0:4050 tells Hypercorn to listen on all available interfaces on port 4050
CMD ["hypercorn", "wsgi:app", "--bind", "0.0.0.0:4050"]