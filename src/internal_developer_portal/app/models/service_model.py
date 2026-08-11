from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ServiceModel(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    port = Column(Integer, nullable=False)
    status = Column(String, default="Aktif")