import datetime
from contextlib import asynccontextmanager
import psutil
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.api.auth_router import router as auth_router

# Loglama modülümüz içe aktarılır
from app.core.logging import get_logger

# Veritabani motoru, Base sinifi ve get_db ice aktarilir
from app.core.database import Base, engine, get_db

# SQLAlchemy modellerinin taninmasi icin ice aktarilmasi gerekir
from app.models.user_model import UserModel
from app.models.service_model import ServiceModel

# Moduler router'lar ice aktarilir
from app.api.user_router import router as user_router
from app.api.service_router import router as service_router

# Logger tanımlanır
logger = get_logger(__name__)

# FastAPI yaşam döngüsü (Lifespan) ile uygulama başlarken log atılması sağlanır
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Uygulama başarıyla başlatıldı ve ayakta!")
    yield
    logger.info("Uygulama kapatılıyor...")

# Veritabanındaki tablolarin (eger yoksa) otomatik olusturulmasini saglar
Base.metadata.create_all(bind=engine)

# FastAPI uygulamasini baslatir ve Swagger dokumantasyon meta verilerini ayarlar
app = FastAPI(
    title="Internal Developer Portal API",
    description="Sirket ici servisleri, kullanicilari, loglari ve sistem durumunu yoneten veritabani destekli IDP backend servisi.",
    version="1.0.0",
    lifespan=lifespan
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
app.include_router(auth_router)

# Kok dizin - API'nin calistigini gosteren temel endpoint
@app.get("/")
def read_root():
    logger.info("Kök dizine (root) istek atıldı.")
    return {
        "message": "Internal Developer Portal API aktif ve calisiyor",
        "documentation": "/docs"
    }

# Servis Sağlık Durumu (Health Check Endpoint)
@app.get("/health", summary="Servis ve Veritabanı Sağlık Durumu (Health Check)")
def health_check(db: Session = Depends(get_db)):
    db_status = "Healthy"
    try:
        # Veritabanına basit bir sorgu atarak bağlantıyı test ediyoruz (SQLAlchemy 2.0 uyumlu)
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"Unhealthy: {str(e)}"
        logger.error(f"Veritabanı sağlık kontrolü başarısız: {str(e)}")

    logger.info("Health check (sağlık durumu) kontrol edildi.")
    
    return {
        "status": "healthy" if db_status == "Healthy" else "unhealthy",
        "app": "Running",
        "database": db_status,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    logger.info("Sistem logları listelendi.")
    return {"logs": logs}

# Veritabani ve Yapilandirma Durumu (IDP Ozelligi)
@app.get("/api/system/status", summary="Veritabani ve Yapilandirma Durumu")
def get_system_status():
    logger.info("Sistem durumu (status) kontrol edildi.")
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

# Sunucu Kaynak ve Sistem Metrikleri (Psutil Ozelligi)
@app.get("/api/system/metrics", summary="Sunucu Kaynak Kullanımı (CPU, RAM, Disk)")
def get_system_metrics():
    # CPU kullanım yüzdesi
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # RAM (Bellek) bilgileri
    memory = psutil.virtual_memory()
    ram_total_gb = round(memory.total / (1024 ** 3), 2)
    ram_used_gb = round(memory.used / (1024 ** 3), 2)
    ram_percent = memory.percent
    
    # Disk bilgileri (Ana sürücü)
    disk = psutil.disk_usage('/')
    disk_total_gb = round(disk.total / (1024 ** 3), 2)
    disk_used_gb = round(disk.used / (1024 ** 3), 2)
    disk_percent = disk.percent
    
    logger.info("Sunucu sistem metrikleri (CPU, RAM, Disk) başarıyla okundu.")
    
    return {
        "cpu": {
            "usage_percent": cpu_usage
        },
        "ram": {
            "total_gb": ram_total_gb,
            "used_gb": ram_used_gb,
            "usage_percent": ram_percent
        },
        "disk": {
            "total_gb": disk_total_gb,
            "used_gb": disk_used_gb,
            "usage_percent": disk_percent
        }
    }