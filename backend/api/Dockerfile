FROM python:3.10-slim

WORKDIR /usr/src/api

ENV FLASK_APP=app/api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=4050
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/api:$PYTHONPATH

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

COPY app/ app/

COPY wsgi.py .
COPY conftest.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4050

CMD ["hypercorn", "wsgi:app", "--bind", "0.0.0.0:4050"]