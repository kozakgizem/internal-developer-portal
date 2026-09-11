from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # <--- Şifreyi sadece oluşturma şemasına ekliyoruz

class UserResponse(UserBase):
    id: int
    username: Optional[str] = None  # Veritabanındaki olası boş (null) kayıtlar için opsiyonel yapıldı

    class Config:
        from_attributes = True