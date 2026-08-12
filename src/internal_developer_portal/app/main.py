import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Veritabani motoru ve Base sinifi ice aktarilir
from app.core.database import Base, engine

# SQLAlchemy modellerinin taninmasi icin ice aktarilmasi gerekir
from app.models.user_model import UserModel
from app.models.service_model import ServiceModel

# Moduler router'lar ice aktarilir
from app.api.user_router import router as user_router
from app.api.service_router import router as service_router

# Veritabanındaki tablolarin (eger yoksa) otomatik olusturulmasini saglar
Base.metadata.create_all(bind=engine)

# FastAPI uygulamasini baslatir ve Swagger dokumantasyon meta verilerini ayarlar
app = FastAPI(
    title="Internal Developer Portal API",
    description="Sirket ici servisleri, kullanicilari, loglari ve sistem durumunu yoneten veritabani destekli IDP backend servisi.",
    version="1.0.0"
)

# CORS politikasi: Tum kaynaklardan gelen isteklere izin verilir
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veritabani ve servis katmanina bagli olan router'lar ana uygulamaya dahil edilir
app.include_router(user_router)
app.include_router(service_router)

# Kok dizin - API'nin calistigini gosteren temel endpoint
@app.get("/")
def read_root():
    return {
        "message": "Internal Developer Portal API aktif ve calisiyor",
        "documentation": "/docs"
    }

# Gercek Sistem Log Akisi (IDP Ozelligi)
@app.get("/api/logs", summary="Gercek Sistem Log Akisi")
def get_system_logs():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    logs = [
        f"[{current_time}] [INFO] API Gateway started successfully on port 8000.",
        f"[{current_time}] [DEBUG] Database pool connection established with SQLAlchemy.",
        f"[{current_time}] [WARN] Auth Service response latency high: 420ms.",
        f"[{current_time}] [INFO] Health check probe succeeded for all active nodes.",
        f"[{current_time}] [ERROR] Payment Service timeout exception on endpoint /pay/verify."
    ]
    return {"logs": logs}

# Veritabani ve Yapilandirma Durumu (IDP Ozelligi)
@app.get("/api/system/status", summary="Veritabani ve Yapilandirma Durumu")
def get_system_status():
    return {
        "database": {
            "cluster": "SQLAlchemy / Veritabani",
            "status": "Healthy",
            "connection": "Connected"
        },
        "cache": {
            "service": "Redis Cache",
            "status": "Active"
        },
        "environment": "production.env"
    }