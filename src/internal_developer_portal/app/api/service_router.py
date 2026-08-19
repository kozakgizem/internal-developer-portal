from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.service_schema import ServiceCreate, ServiceResponse
from app.services.service_service import ServiceService
import logging

# Arka planda çalışacak örnek audit log / bildirim fonksiyonu
def log_service_creation_to_audit(service_name: str):
    logger = logging.getLogger("app.background")
    logger.info(f"[AUDIT LOG] Yeni mikroservis başarıyla sisteme tanımlandı: '{service_name}'")
    print(f"--> [BACKGROUND TASK] '{service_name}' için audit log ve bildirim işlemleri tamamlandı.")

# Servis rotalarını gruplamak için router nesnesi oluşturulur (Swagger'da /services altında görünür)
router = APIRouter(prefix="/services", tags=["Services"])

# Yeni servis oluşturma endpoint'i (POST isteği)
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service: ServiceCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # iş mantığını yönetmesi için ServiceService katmanı çağrılır
    new_service = ServiceService.create_service(db=db, service=service)
    
    # Kullanıcıyı hiç bekletmeden, arka planda çalışacak audit log görevini kuyruğa ekliyoruz
    background_tasks.add_task(log_service_creation_to_audit, service.name)
    
    return new_service

# Servisleri listeleme endpoint'i (GET isteği)
@router.get("/", response_model=list[ServiceResponse])
def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Kayıtlı tüm servisleri sayfalı şekilde getirmek için servis katmanı çağrılır
    return ServiceService.get_services(db=db, skip=skip, limit=limit)