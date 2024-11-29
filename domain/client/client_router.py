from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from domain.client.client_schema import ClientCreate, ClientUpdate, ClientResponse
from database import get_db, Client


router = APIRouter()


@router.post("/client/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """
    Create/Post new client
    """
    # check state in range
    if not valid_states(client.state):
        raise HTTPException(
            status_code=400,
            detail=f"I'm sorry, {client.state} is not within our service range",
        )

    # format state to abbreviation
    formatted_state = format_state(client.state)

    db_client = Client(
        name=client.name,
        email=client.email,
        event_type=client.event_type,
        address=client.address,
        city=client.city,
        state=formatted_state,
        date=client.date,
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/client/", response_model=list[ClientResponse])
def read_clients(db: Session = Depends(get_db)):
    """
    Get all clients
    """
    clients = db.query(Client).all()
    return clients


@router.get("/client/{client_id}", response_model=ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    """
    get one client
    """
    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.get("/client/sort/{direction}", response_model=list[ClientResponse])
def sort_by_date(direction: str, db: Session = Depends(get_db)):
    """
    sort client event dates ascending or descending
    """
    if direction == "asc":
        clients = db.query(Client).order_by(Client.date.asc()).all()
        return clients

    clients = db.query(Client).order_by(Client.date.desc()).all()
    return clients


@router.put("/client/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    """
    Update/Put client
    """
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    if not valid_states(client.state):
        raise HTTPException(
            status_code=400,
            detail=f"I'm sorry, {client.state} is not within our service range",
        )

    formatted_state = format_state(client.state)

    db_client.name = client.name
    db_client.email = client.email
    db_client.event_type = client.event_type
    db_client.address = client.address
    db_client.city = client.city
    db_client.state = formatted_state
    db_client.date = client.date

    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/client/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    Delete client
    """
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(db_client)
    db.commit()
    return {"detail": "Client deleted successfully"}


# -----------------------------------------------------------------------
#            Utilities
# -----------------------------------------------------------------------


def valid_states(state: str) -> bool:
    """
    Determines if a state is a valid state (distance),
    otherwise the event cannot be accepted
    """
    valid_states = {
        "pa",
        "pennsylvania",
        "nj",
        "new jersey",
        "ny",
        "new york",
        "de",
        "delaware",
        "md",
        "maryland",
    }

    return state.lower() in valid_states


def format_state(state: str) -> str:
    """
    Returns a unified state format (PA)
    """

    state_dico = {
        "pennsylvania": "PA",
        "new jersey": "NJ",
        "new york": "NY",
        "delaware": "DE",
        "maryland": "MD",
    }

    if len(state) == 2:
        return state.upper()

    return state_dico[state.lower()]
