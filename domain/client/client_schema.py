from pydantic import BaseModel
from datetime import date


# Pydantic schemas
class ClientCreate(BaseModel):
    name: str
    email: str
    event_type: str
    address: str
    city: str
    state: str
    date: date


class ClientUpdate(BaseModel):
    name: str
    email: str
    event_type: str
    address: str
    city: str
    state: str
    date: date


class ClientResponse(ClientCreate):
    id: int
