from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # <--- Şifreyi sadece oluşturma şemasına ekliyoruz

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True