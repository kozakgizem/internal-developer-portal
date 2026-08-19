from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash
from fastapi import HTTPException, status

class UserService:
    
    # Yeni kullanıcı oluşturma iş kurallarını yöneten statik metot
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # 1. İş Kuralı: Aynı e-posta adresiyle başka bir kullanıcı var mı kontrol edilir
        existing_user = UserRepository.get_user_by_email(db, email=user.email)
        
        if existing_user:
            # Eğer kullanıcı zaten varsa, API üzerinden 400 hatası döndürülür
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu e-posta adresiyle kayıtlı bir kullanıcı zaten mevcut."
            )
        
        # Kullanıcının girdiği düz şifre güvenli bir şekilde hash'lenir
        hashed_password = get_password_hash(user.password)
        
        # 2. İş kuralı başarılıysa, repository katmanı çağrılarak veritabanına kayıt yapılır
        return UserRepository.create_user(db, user=user, hashed_password=hashed_password)