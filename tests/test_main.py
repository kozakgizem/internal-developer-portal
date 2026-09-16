import sys
import os

# Doğrudan 'src' klasörünü arama yolunun en başına ekliyoruz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/internal_developer_portal')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# GET /health - Servis ve Veritabanı Sağlık Durumu
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

# GET / - Read Root (Ana Dizin)
def test_root_accessible():
    response = client.get("/")
    assert response.status_code in [200, 404]

# GET /docs - Swagger UI Dokümantasyonu
def test_docs_accessible():
    response = client.get("/docs")
    assert response.status_code == 200

# --- Users Endpointleri ---

# GET /users/ - Kullanıcıları Listeleme
def test_get_users():
    response = client.get("/users/")
    assert response.status_code in [200, 401, 403, 422]

# POST /users/ - Yeni Kullanıcı Oluşturma
def test_create_user_invalid_payload():
    response = client.post("/users/", json={})
    assert response.status_code in [400, 401, 422]

# GET /users/me - Mevcut Kullanıcı Bilgisi
def test_get_current_user_me():
    response = client.get("/users/me")
    assert response.status_code in [200, 401, 403]

# --- Services Endpointleri ---

# GET /services/ - Servisleri Listeleme
def test_get_services():
    response = client.get("/services/")
    assert response.status_code in [200, 401, 403, 422]

# POST /services/ - Yeni Servis Oluşturma
def test_create_service_invalid_payload():
    response = client.post("/services/", json={})
    assert response.status_code in [400, 401, 422]

# --- Management & Config Endpointleri ---

# GET /management/config/json - JSON Konfigürasyonunu Getir
def test_management_config_get():
    response = client.get("/management/config/json")
    assert response.status_code in [200, 401, 403]

# PUT /management/config/json - JSON Konfigürasyonunu Güncelle
def test_management_config_put_invalid():
    response = client.put("/management/config/json", json={})
    assert response.status_code in [200, 400, 401, 422]

# GET /management/services/yaml - YAML Servislerini Getir
def test_management_services_yaml():
    response = client.get("/management/services/yaml")
    assert response.status_code in [200, 401, 403]

# --- System & Logs Endpointleri ---

# GET /api/logs - Gerçek Sistem Log Akışı
def test_api_logs():
    response = client.get("/api/logs")
    assert response.status_code in [200, 401, 403]

# GET /api/system/status - Veritabanı ve Yapılandırma Durumu
def test_system_status():
    response = client.get("/api/system/status")
    assert response.status_code in [200, 401, 403]

# GET /api/system/metrics - Sunucu Kaynak Kullanımı (CPU, RAM, Disk)
def test_system_metrics():
    response = client.get("/api/system/metrics")
    assert response.status_code in [200, 401, 403]

# --- Authentication Endpointleri ---

# POST /auth/token - Kullanıcı Girişi ve JWT Token Alma
def test_auth_token_invalid():
    response = client.post("/auth/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code in [400, 401, 422]