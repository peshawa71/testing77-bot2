FROM python:3.11

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

CMD ["python", "main.py"]
