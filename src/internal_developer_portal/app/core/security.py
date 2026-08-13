from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Gizli anahtar ve algoritma (Gerçek projelerde çevre değişkenlerinde .env içinde saklanır)
SECRET_KEY = "gizli-anahtar-buraya-gelecek-cok-gizli-bir-metin"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Şifre hashleme (şifreleme) yöneticisi
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kullanıcının girdiği düz şifre ile veritabanındaki hashlenmiş şifreyi karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Düz şifreyi güvenli bir şekilde hashler."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Kullanıcı için süreli bir JWT Token üretir."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt