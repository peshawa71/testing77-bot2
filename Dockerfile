RUN apt-get update && apt-get install -y ffmpeg
a# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Optional: Prevent ImageMagick security policy errors
RUN sed -i 's/rights="none"/rights="read|write"/g' /etc/ImageMagick-6/policy.xml || true

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your app code into the container
COPY . .

# Default command (change to match your app)
CMD ["python", "main.py"]
