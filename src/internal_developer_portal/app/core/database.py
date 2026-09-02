from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Merkezi config'den (settings) veritabanı URL'ini alıyoruz
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# FastAPI Endpoint'lerinde veritabanı oturumunu yönetmek için bağımlılık
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()