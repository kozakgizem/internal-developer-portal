from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService
from app.core.security import get_current_user
from app.models.user_model import UserModel

# API rotalarını gruplamak için router nesnesi oluşturulur (Swagger'da /users altında görünür)
router = APIRouter(prefix="/users", tags=["Users"])

# Yeni kullanıcı oluşturma endpoint'i (POST isteği)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # İş mantığını yönetmesi için UserService katmanı çağrılır
    return UserService.create_user(db=db, user=user)

# Giriş yapmış kullanıcının bilgilerini getiren JWT korumalı endpoint
@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    """
    Giriş yapmış olan kullanıcının bilgilerini döndürür (JWT korumalıdır).
    """
    return current_user