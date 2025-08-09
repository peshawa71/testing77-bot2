FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg imagemagick libx11-dev && \
    pip install --no-cache-dir moviepy
