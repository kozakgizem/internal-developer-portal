from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService

# API rotalarını gruplamak için router nesnesi oluşturulur (Swagger'da /users altında görünür)
router = APIRouter(prefix="/users", tags=["Users"])

# Yeni kullanıcı oluşturma endpoint'i (POST isteği)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # İş mantığını yönetmesi için UserService katmanı çağrılır
    return UserService.create_user(db=db, user=user)