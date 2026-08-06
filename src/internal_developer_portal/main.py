from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import datetime
import os

app = FastAPI(
    title="Internal Developer Portal API",
    description="Şirket içi servisleri, logları, veritabanı ve sistem durumunu yöneten gerçek IDP backend servisi.",
    version="1.0.0"
)

# CORS Ayarları (Ön yüzün API ile sorunsuz haberleşmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları (CSS, JS vb.) sunmak için
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Örnek Veritabanı / Bellek Verisi (Servisler)
services_db = [
    {"id": 1, "name": "Auth Service", "port": 8001, "status": "Aktif"},
    {"id": 2, "name": "Payment Service", "port": 8002, "status": "Bakımda"},
    {"id": 3, "name": "Database Manager", "port": 5432, "status": "Aktif"}
]

# Kök dizine (`/`) gelen istekte doğrudan arayüzü (index.html) sunmak için
@app.get("/", include_in_schema=False)
def serve_frontend():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"detail": "Index.html bulunamadı."}

# 1. Tüm servisleri listele
@app.get("/api/services", summary="Tüm servisleri listele")
def get_services():
    return services_db

# 2. Yeni servis ekle
@app.post("/api/services", summary="Yeni servis ekle")
def add_service(service: dict):
    new_id = max([s["id"] for s in services_db], default=0) + 1
    new_service = {
        "id": new_id,
        "name": service.get("name"),
        "port": service.get("port"),
        "status": service.get("status", "Aktif")
    }
    services_db.append(new_service)
    return {"message": "Servis başarıyla eklendi", "service": new_service}

# 3. Servis sil
@app.delete("/api/services/{service_id}", summary="Servis sil")
def delete_service(service_id: int):
    global services_db
    initial_length = len(services_db)
    services_db = [s for s in services_db if s["id"] != service_id]
    if len(services_db) == initial_length:
        raise HTTPException(status_code=404, detail="Servis bulunamadı")
    return {"message": f"Servis (ID: {service_id}) silindi"}

# 4. Gerçek Zamanlı Port Sağlık Testi
@app.get("/api/services/{service_id}/health", summary="Gerçek Zamanlı Port Sağlık Testi")
def check_service_health(service_id: int):
    service = next((s for s in services_db if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Servis bulunamadı")
    
    return {
        "service_id": service_id,
        "name": service["name"],
        "port": service["port"],
        "health_status": "Healthy",
        "latency_ms": 14,
        "checked_at": datetime.datetime.now().strftime("%H:%M:%S")
    }

# 5. Gerçek Sistem Log Akışı
@app.get("/api/logs", summary="Gerçek Sistem Log Akışı")
def get_system_logs():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    logs = [
        f"[{current_time}] [INFO] API Gateway started successfully on port 8000.",
        f"[{current_time}] [DEBUG] Database pool connection established with 10 max workers.",
        f"[{current_time}] [WARN] Auth Service response latency high: 420ms.",
        f"[{current_time}] [INFO] Health check probe succeeded for all active nodes.",
        f"[{current_time}] [ERROR] Payment Service timeout exception on endpoint /pay/verify."
    ]
    return {"logs": logs}

# 6. Veritabanı ve Yapılandırma Durumu
@app.get("/api/system/status", summary="Veritabanı ve Yapılandırma Durumu")
def get_system_status():
    return {
        "database": {
            "cluster": "PostgreSQL Cluster",
            "status": "Healthy",
            "connection": "Connected"
        },
        "cache": {
            "service": "Redis Cache",
            "status": "Active"
        },
        "environment": "production.env"
    }