FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir cassandra-driver
COPY . .
CMD ["python", "app.py"]