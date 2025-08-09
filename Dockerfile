# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed by moviepy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy (avoids 'not authorized' error)
RUN sed -i 's/rights="none"/rights="read|write"/g' /etc/ImageMagick-6/policy.xml || true

# Install moviepy and its required Python libraries
RUN pip install --no-cache-dir moviepy

# Optional: Copy your local files into the container
# COPY . .

# Set default command (update if needed)
CMD ["python3"]
