from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.service_schema import ServiceCreate, ServiceResponse
from app.services.service_service import ServiceService

# Servis rotalarını gruplamak için router nesnesi oluşturulur (Swagger'da /services altında görünür)
router = APIRouter(prefix="/services", tags=["Services"])

# Yeni servis oluşturma endpoint'i (POST isteği)
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    # İş mantığını yönetmesi için ServiceService katmanı çağrılır
    return ServiceService.create_service(db=db, service=service)

# Servisleri listeleme endpoint'i (GET isteği)
@router.get("/", response_model=list[ServiceResponse])
def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Kayıtlı tüm servisleri sayfalı şekilde getirmek için servis katmanı çağrılır
    return ServiceService.get_services(db=db, skip=skip, limit=limit)