FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get clean

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "app/main.py"]
