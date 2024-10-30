from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from domain.client.client_schema import ClientCreate, ClientUpdate, ClientResponse
from database import get_db, Client


router = APIRouter()



def valid_states(state:str) -> bool:
    """
    Determines if a state is a valid state (distance), 
    otherwise the event cannot be accepted
    """
    valid_states = {'pa', 'pennsylvania', 'nj', 'new jersey', 'ny', 'new york', 'de', 'delaware', 'md', 'maryland'}

    return state.lower() in valid_states
        


@router.post("/client/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    print()
    print(client)
    print()
    if not valid_states(client.state):
        raise HTTPException(status_code=400, detail=f"I'm sorry, {client.state} is not within our service range")
    db_client = Client(
        name=client.name,
        email=client.email,
        address=client.address,
        city=client.city,
        state=client.state,
        date=client.date,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    print(db_client)
    return db_client


@router.get("/client/", response_model=list[ClientResponse])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients


@router.get("/client/{client_id}", response_model=ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/client/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db_client.name = client.name
    db_client.email = client.email
    db_client.address = client.address
    db_client.city = client.city
    db_client.state = client.state
    db_client.date = client.date
    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/client/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(db_client)
    db.commit()
    return {"detail": "Client deleted successfully"}
