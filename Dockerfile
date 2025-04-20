FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential \
    alsa-utils\
    libasound2\
    ffmpeg\
    espeak && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -v --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV DEBUG=FALSE
ENV PORT=5000
ENV LOG_FILE=/data/logs/logs.txt

CMD ["python", "run.py"]