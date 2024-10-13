# Use the official TensorFlow GPU image as the base image
FROM tensorflow/tensorflow:2.12.0-gpu

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# libsndfile1 is required for audio file processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./app .

# Set the command to run the application
CMD ["python", "main.py"]
