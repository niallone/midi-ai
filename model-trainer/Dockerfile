#FROM python:3.10-slim

# For H100 training
FROM tensorflow/tensorflow:2.12.0-gpu

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["python", "model_generator_cli.py", "/app/input", "/app/model"]



# sudo nvidia-ctk runtime configure --runtime=docker
