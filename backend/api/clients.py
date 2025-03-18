# File: backend/api/clients.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from models import Client, User
# from database import get_db
# from auth import get_current_user

# router = APIRouter()


# @router.get("/clients")
# def get_clients(
#     db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
# ):
#     """Returns only the clients belonging to the logged-in user"""
#     clients = db.query(Client).filter(Client.user_id == current_user.id).all()
#     return {"clients": clients}


# @router.post("/clients")
# def create_client(
#     client_data: dict,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """Creates a new client linked to the logged-in user"""
#     new_client = Client(name=client_data["name"], user_id=current_user.id)
#     db.add(new_client)
#     db.commit()
#     db.refresh(new_client)
#     return {"message": "Client created successfully", "client": new_client}
