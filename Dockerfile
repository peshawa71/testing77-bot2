FROM python:3.11

COPY . /app

RUN pip install --no-cache-dir moviepy imageio[ffmpeg]

CMD ["python", "main.py"]
