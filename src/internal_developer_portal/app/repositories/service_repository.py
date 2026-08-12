# SQLAlchemy oturum nesnesi içe aktarılır
from sqlalchemy.orm import Session

# Servis tablosunu temsil eden ORM modeli içe aktarılır (ServiceModel kullanıldı)
from app.models.service_model import ServiceModel

# Dışarıdan gelecek servis verilerinin şeması içe aktarılır
from app.schemas.service_schema import ServiceCreate

class ServiceRepository:
    
    # Tüm servisleri listeleyen statik metot
    @staticmethod
    def get_services(db: Session, skip: int = 0, limit: int = 100):
        # Servis tablosundaki kayıtları sayfalama (skip/limit) desteğiyle getirir
        return db.query(ServiceModel).offset(skip).limit(limit).all()

    # Yeni servis oluşturan ve veritabanına kaydeden statik metot
    @staticmethod
    def create_service(db: Session, service: ServiceCreate):
        # Gelen şema verileriyle yeni bir ServiceModel nesnesi üretilir
        db_service = ServiceModel(name=service.name, port=service.port, status=service.status)
        
        # Oturuma eklenir
        db.add(db_service)
        
        # Veritabanına kaydedilir
        db.commit()
        
        # ID gibi otomatik alanların nesneye yansıması sağlanır
        db.refresh(db_service)
        
        # Kaydedilen servis nesnesi döndürülür
        return db_service