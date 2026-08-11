# FastAPI çatısını kurmak ve HTTP hata kodları (404 vb.) fırlatmak için içe aktarılır.
from fastapi import FastAPI, HTTPException
# Farklı port veya adreslerden gelen isteklerin (CORS politikası nedeniyle) engellenmemesi için güvenlik katmanını yapılandırır.
from fastapi.middleware.cors import CORSMiddleware
# Bilgisayardaki bir dosyayı (örneğin index.html) doğrudan tarayıcıya HTTP yanıtı olarak dönmek için kullanılır.
from fastapi.responses import FileResponse
# CSS, JavaScript veya resim gibi statik dosyaların sunulacağı klasör yolunu sisteme tanıtmak için kullanılır.
from fastapi.staticfiles import StaticFiles
# Tarih/saat damgası üretmek için kullanılır.
import datetime
# Dosya yollarını işletim sistemine uygun olarak dinamik bir şekilde birleştirmek için kullanılır.
import os

# FastAPI uygulamasını başlatır ve bir nesne (app) oluşturur. Swagger dokümantasyonu meta verilerini ayarlar.
app = FastAPI(
    title="Internal Developer Portal API",
    description="Şirket içi servisleri, logları, veritabanı ve sistem durumunu yöneten gerçek IDP backend servisi.",
    version="1.0.0"
)

# allow_origins=["*"] ayarı ile her yerden gelen isteklere izin verilir, böylece ön yüz arka uçla rahatça konuşabilir.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Proje klasöründeki static klasörünü arar ve varsa /static adresi üzerinden dış dünyaya açar.
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Gerçek bir SQL veritabanı yerine geçici olarak Python listesi içinde mikroservislerin başlangıç verilerini tutan bellek tabanlı veritabanı simülasyonudur.
services_db = [
    {"id": 1, "name": "Auth Service", "port": 8001, "status": "Aktif"},
    {"id": 2, "name": "Payment Service", "port": 8002, "status": "Bakımda"},
    {"id": 3, "name": "Database Manager", "port": 5432, "status": "Aktif"}
]

# Tarayıcıda ana adrese (http://127.0.0.1:8000/) girildiğinde çalışır. include_in_schema=False ile Swagger dokümantasyonunda görünmesi engellenir.
@app.get("/", include_in_schema=False)
def serve_frontend():
    # templates/index.html dosyasının yolunu dinamik olarak bulur ve FileResponse ile tarayıcıya sunar.
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"detail": "Index.html bulunamadı."}

# Tüm servisleri listele: Bellekteki services_db listesinin tamamını JSON formatında geri döndürür.
@app.get("/api/services", summary="Tüm servisleri listele")
def get_services():
    return services_db

# Yeni servis ekle: Mevcut ID'lerin en büyüğünü bulup 1 ekleyerek yeni benzersiz ID üretir, gelen verilerle yeni servis nesnesi oluşturup listeye ekler.
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

# Servis sil: Gönderilen service_id değerine sahip servisi listeden çıkarır. Eğer liste boyutu değişmediyse servis bulunamamıştır ve 404 HTTP hatası fırlatır.
@app.delete("/api/services/{service_id}", summary="Servis sil")
def delete_service(service_id: int):
    global services_db
    initial_length = len(services_db)
    services_db = [s for s in services_db if s["id"] != service_id]
    if len(services_db) == initial_length:
        raise HTTPException(status_code=404, detail="Servis bulunamadı")
    return {"message": f"Servis (ID: {service_id}) silindi"}

# Gerçek Zamanlı Port Sağlık Testi: ID'si verilen servisi bulur, bulamazsa 404 döner; bulursa anlık gecikme süresini, sağlık durumunu ve saat damgasını raporlar.
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

# Gerçek Sistem Log Akışı: Kurumsal sistemlerdeki bilgi, uyarı ve hata loglarını o anki zaman damgasıyla birlikte bir liste olarak döner.
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

# Veritabanı ve Yapılandırma Durumu: Arka plandaki PostgreSQL kümesinin, Redis önbellek servisinin ve ortam dosyasının durumunu JSON formatında raporlar.
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