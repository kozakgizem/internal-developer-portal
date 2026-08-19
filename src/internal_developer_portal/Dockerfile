# Hafif ve güvenli bir Python imajı kullanıyoruz
FROM python:3.10-slim

# Konteyner içerisindeki çalışma dizinini /app yapıyoruz
WORKDIR /app

# Bağımlılık dosyasını kopyalayıp kütüphaneleri yüklüyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projedeki tüm dosyaları konteynere kopyalıyoruz
COPY . .

# src klasörünün Python tarafından tanınması için PYTHONPATH ayarlıyoruz
ENV PYTHONPATH=/app/src

# Uygulamayı Uvicorn ile dış dünyaya açıyoruz
CMD ["uvicorn", "internal_developer_portal.app.main:app", "--host", "0.0.0.0", "--port", "8000"]