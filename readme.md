# AI Melody Generator

## Overview

AI Melody Generator is a web application that trains and uses artificial intelligence neural networks to create unique musical melodies. The project consists of a React-based frontend, a Flask-based backend API, and a model trainer component. 

You can try it out at [melodygenerator.fun](https://melodygenerator.fun).

## Features

- Generate unique melodies using AI models
- Play and visualise generated melodies
- Download generated melodies as MIDI files
- Multiple AI models trained on different genres

## Technology Stack

- Frontend: React, Next.js
- Backend: Quart/Flask (Python)
- AI: TensorFlow, Keras
- Database: PostgreSQL
- Containerisation: Docker Compose

## Project Structure

- `frontend/`: React frontend application
- `backend/`: Flask API and model serving
- `model-trainer/`: Scripts for training melody generation models
- `models/`: Trained AI models and training data

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local frontend development)
- Python 3.10+ (for local backend development)

## Models

The AI Melody Generator currently uses the following models:

- V2: Trained on 25 R&B/90s Hip Hop songs
- V3: Trained on about 200 Dance songs
- V4: (Upcoming) To be trained on about 200 jazz songs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Known Issues

 - Sound on mobile needs to be tested, this may be a bug.
 - Play/pause with multiple files (Also play/pause on multiple files sequentially, and play/pause/generate combinations)

