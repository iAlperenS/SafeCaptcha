# Python base image
FROM python:3.13.2-slim

# Ortam değişkeni
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizini
WORKDIR /app

# Gereksinimler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Port
EXPOSE 5000

# Başlatıcı komut
CMD ["python", "run.py"]
