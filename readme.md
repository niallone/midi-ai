# AI Melody Generator

## Overview

AI Melody Generator is a web application that trains and uses artificial intelligence neural networks to create unique musical melodies. The project consists of a Next/React-based frontend, a Quart/Flask-based backend API, and a model trainer component. 

You can try it out at [melodygenerator.fun](https://melodygenerator.fun).

## Features

- Generate unique melodies using AI models
- Play and visualise generated melodies
- Download generated melodies as MIDI files
- Multiple AI models trained on different genres

## Technology Stack

- Frontend: React, Next.js
- Backend: Hypercorn WSGI/Quart/Flask (Python)
- AI: TensorFlow, Keras
- Database: PostgreSQL
- Containerisation: Docker Compose

## Project Structure

- `frontend/`: React frontend application
- `backend/`: Flask API and Postgres
- `model-trainer/`: Scripts for training melody generation models
- `models/`: Trained AI models and training data

## Models

The AI Melody Generator currently uses the following models:

- V2: Trained on 25 R&B/90s hip hp songs
- V3: Trained on about 200 dance songs
- V4: Trained on about 180 jazz songs
- V5: Trained on 275 Songs from various genres and decades.

### Model Training

The `model-trainer` service is setup to be run on an NVIDIA H100. To run on local machine change the Dockerfile image to Python 10 and comment out the `deploy` section in the `docker-compose.yml`.

The docker runtime can be configured to the NIVDIA runtime with the command `nvidia-ctk runtime configure --runtime=docker`.

This should give the container access to the GPU. This can be tested by running `nvidia-smi` from the container.

## Known Issues

 - Sound on mobile doesn't work due to midi compatibility on devices. Currently investigating mobile solution.
 - Play/pause with multiple files (Also play/pause on multiple files sequentially, and play/pause/generate combinations)

