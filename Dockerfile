# Use an official Python base image
FROM python:3.11-slim

# Install system dependencies (moviepy depends on ffmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install moviepy via pip
RUN pip install --no-cache-dir moviepy

# Set working directory to root (optional, default is / anyway)
WORKDIR /

# Copy any needed files (optional, only if you have something to run)
# COPY your_script.py .

# Default command (can be changed)
CMD ["python3"]
