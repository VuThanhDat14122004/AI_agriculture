FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cow_project

COPY requirements.txt .
COPY app /cow_project/app
COPY app/best.pt /cow_project/app/best.pt

COPY templates /cow_project/app/templates

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app/main.py"]
