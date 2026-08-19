# SQLAlchemy üzerinden veritabanı işlemlerini (sorgu atma, kaydetme vb.) yürütmemizi sağlayan oturum nesnesi içe aktarılır
from sqlalchemy.orm import Session

# Veritabanındaki users tablosunu temsil eden SQLAlchemy ORM modeli içe aktarılır
from app.models.user_model import UserModel

# Dışarıdan gelecek kullanıcı verilerinin kurallarını ve şemasını kontrol eden Pydantic modeli içe aktarılır
from app.schemas.user_schema import UserCreate

class UserRepository:
    
    # E-posta adresine göre veritabanından kullanıcı sorgulayan statik metot
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        # UserModel tablosunda gelen email ile eşleşen ilk kaydı döndürür
        return db.query(UserModel).filter(UserModel.email == email).first()

    # Pydantic şemasından gelen verilerle yeni kullanıcı oluşturan ve veritabanına kaydeden statik metot
    @staticmethod
    def create_user(db: Session, user: UserCreate, hashed_password: str):
        # Gelen verilerle SQLAlchemy ORM model nesnesi üretilir (UserModel kullanıldı)
        db_user = UserModel(
            username=user.username, 
            email=user.email, 
            hashed_password=hashed_password
        )
        
        # Nesne veritabanı oturumuna eklenir
        db.add(db_user)
        
        # Değişiklikler veritabanına kalıcı olarak kaydedilir (commit edilir)
        db.commit()
        
        # Veritabanında otomatik üretilen (ID gibi) alanların nesneye yansıması sağlanır
        db.refresh(db_user)
        
        # Kaydedilen yeni kullanıcı nesnesi geri döndürülür
        return db_user