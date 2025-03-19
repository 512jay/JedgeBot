from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.data.models import ClientAccount as Client, User
from backend.data.auth_database import get_db
from backend.api.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()


class ClientCreate(BaseModel):
    name: str


@router.get("/test")
def test_endpoint():
    return {"message": "Clients API is working"}


@router.get("/clients")
def get_clients(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Returns only the clients belonging to the logged-in user"""
    clients = db.query(Client).filter(Client.client_id == current_user.user_id).all()
    return {"clients": clients}


@router.post("/clients")
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Creates a new client linked to the logged-in user"""
    new_client = Client(broker_name=client_data.name, client_id=current_user.user_id)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"message": "Client created successfully", "client": new_client}
