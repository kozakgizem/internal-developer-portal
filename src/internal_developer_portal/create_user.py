from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user_model import UserModel
from app.core.security import get_password_hash

# Tabloları oluştur (eğer yoksa)
Base.metadata.create_all(bind=engine)

def create_initial_user():
    db = SessionLocal()
    # Test kullanıcısı
    email = "test@example.com"
    password = "password123"
    
    # Kullanıcı zaten var mı kontrol et
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        new_user = UserModel(email=email, hashed_password=get_password_hash(password))
        db.add(new_user)
        db.commit()
        print(f"Kullanıcı oluşturuldu: {email}")
    else:
        print("Kullanıcı zaten mevcut.")
    db.close()

if __name__ == "__main__":
    create_initial_user()