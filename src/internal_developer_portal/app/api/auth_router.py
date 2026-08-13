from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user_model import UserModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", summary="Kullanıcı Girişi ve JWT Token Alma")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Veritabanından kullanıcıyı e-posta (username alanına e-posta giriliyor varsayıyoruz) ile arıyoruz
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # Kullanıcı yoksa veya şifre yanlışsa hata fırlatıyoruz
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz e-posta veya şifre",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token süresini belirleyip erişim token'ı üretiyoruz
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}