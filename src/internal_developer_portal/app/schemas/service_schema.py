from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    port: int
    status: str = "Aktif"

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True