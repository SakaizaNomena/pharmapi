from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.core.security import get_current_user
from src.app.schemas.pharmacy_schema import PharmacyItem
from src.app.schemas.user_schema import (
    UserCreate,
    UserItem,
    UserUpdate,
    UserWithPharmacies,
)
from src.app.services import user_services

# Tag "users" : regroupe toutes les routes utilisateurs dans /docs.
# dependencies=[Depends(get_current_user)] protège TOUTES les routes :
# sans token valide, l'API renvoie 401 Unauthorized.
router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)


# GET /users/ : liste de tous les utilisateurs.
@router.get("/", response_model=List[UserItem])
def get_users(db: Session = Depends(get_db)):
    return user_services.get_all_users(db)


# GET /users/{user_id} : un utilisateur + ses pharmacies.
@router.get("/{user_id}", response_model=UserWithPharmacies)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_services.get_user(db, user_id)


# POST /users/ : créer un utilisateur.
@router.post("/", response_model=UserItem, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_services.create_user(db, user)


# PUT /users/{user_id} : modifier un utilisateur.
@router.put("/{user_id}", response_model=UserItem)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_services.update_user(db, user_id, user)


# DELETE /users/{user_id} : supprimer un utilisateur.
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_services.delete_user(db, user_id)


# GET /users/{user_id}/pharmacies : pharmacies liées à un utilisateur.
@router.get("/{user_id}/pharmacies", response_model=List[PharmacyItem])
def get_user_pharmacies(user_id: int, db: Session = Depends(get_db)):
    return user_services.get_user_pharmacies(db, user_id)


# POST /users/{user_id}/pharmacies/{pharmacy_id} : lier une pharmacie.
@router.post("/{user_id}/pharmacies/{pharmacy_id}", response_model=UserWithPharmacies)
def attach_pharmacy(user_id: int, pharmacy_id: int, db: Session = Depends(get_db)):
    return user_services.attach_pharmacy(db, user_id, pharmacy_id)


# DELETE /users/{user_id}/pharmacies/{pharmacy_id} : retirer le lien.
@router.delete("/{user_id}/pharmacies/{pharmacy_id}", response_model=UserWithPharmacies)
def detach_pharmacy(user_id: int, pharmacy_id: int, db: Session = Depends(get_db)):
    return user_services.detach_pharmacy(db, user_id, pharmacy_id)
