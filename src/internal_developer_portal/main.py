from fastapi import FastAPI
from internal_developer_portal.models import Service, ServiceCreate

app = FastAPI(title="Internal Developer Portal")

# Örnek başlangıç verilerimiz
SERVICES = [
    Service(id=1, name="Auth Service", status="Aktif", port=8001),
    Service(id=2, name="Payment Service", status="Bakımda", port=8002),
    Service(id=3, name="Database Manager", status="Aktif", port=5432),
]

@app.get("/")
def read_root():
    return {"message": "Internal Developer Portal'a Hoş Geldiniz! 🚀"}

@app.get("/api/services")
def get_services():
    return {"services": SERVICES}

@app.post("/api/services")
def create_service(new_service: ServiceCreate):
    new_id = max([s.id for s in SERVICES]) + 1 if SERVICES else 1
    
    service_item = Service(
        id=new_id,
        name=new_service.name,
        status=new_service.status,
        port=new_service.port
    )
    SERVICES.append(service_item)
    
    return {"message": "Servis başarıyla eklendi!", "service": service_item}