from sqlalchemy.orm import Session
from app.repositories.service_repository import ServiceRepository
from app.schemas.service_schema import ServiceCreate

class ServiceService:
    
    # Tüm servisleri listeleyen iş mantığı metodu
    @staticmethod
    def get_services(db: Session, skip: int = 0, limit: int = 100):
        # Repository katmanı çağrılarak veriler getirilir
        return ServiceRepository.get_services(db, skip=skip, limit=limit)

    # Yeni servis oluşturma iş kurallarını yöneten metot
    @staticmethod
    def create_service(db: Session, service: ServiceCreate):
        # Gerekirse burada "aynı isimde servis var mı?" gibi iş kuralları eklenebilir.
        # Şimdilik doğrudan repository katmanı üzerinden kayıt işlemi gerçekleştirilir.
        return ServiceRepository.create_service(db=db, service=service)