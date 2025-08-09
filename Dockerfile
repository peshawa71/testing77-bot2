# Use a minimal Python base image
FROM python:3.11-slim

# Install system packages needed for moviepy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy (avoids "not authorized" error)
RUN sed -i 's/rights="none"/rights="read|write"/g' /etc/ImageMagick-6/policy.xml || true

# Install moviepy and related Python packages
RUN pip install --no-cache-dir moviepy

# Copy your entire project (optional if you're just testing)
COPY . .

# Default command to run when container starts
CMD ["python3"]
