from pydantic import BaseModel
from datetime import date

# Pydantic schemas
class ClientCreate(BaseModel):
    name: str
    email: str
    address: str
    city: str
    state: str
    date: date

class ClientUpdate(BaseModel):
    name: str
    email: str
    address: str
    city: str
    state: str
    date: date

class ClientResponse(ClientCreate):
    id: int