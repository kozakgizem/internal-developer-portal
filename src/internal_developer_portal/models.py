from pydantic import BaseModel

class Service(BaseModel):
    id: int
    name: str
    status: str
    port: int

class ServiceCreate(BaseModel):
    name: str
    status: str
    port: int