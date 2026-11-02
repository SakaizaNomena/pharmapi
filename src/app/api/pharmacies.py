from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.schemas.pharmacy_schema import (
    PharmacyCreate,
    PharmacyItem,
    PharmacyUpdate,
)
from src.app.schemas.user_schema import UserItem
from src.app.services import pharmacy_services

# Tag "pharmacies" : regroupe toutes les routes pharmacies dans /docs.
router = APIRouter(
    prefix="/pharmacies",
    tags=["pharmacies"],
)


# GET /pharmacies/ : liste de toutes les pharmacies.
@router.get("/", response_model=List[PharmacyItem])
def get_pharmacies(db: Session = Depends(get_db)):
    return pharmacy_services.get_all_pharmacies(db)


# GET /pharmacies/{pharmacy_id} : une pharmacie par son id.
@router.get("/{pharmacy_id}", response_model=PharmacyItem)
def get_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)):
    return pharmacy_services.get_pharmacy(db, pharmacy_id)


# POST /pharmacies/ : créer une pharmacie.
@router.post("/", response_model=PharmacyItem, status_code=201)
def create_pharmacy(pharmacy: PharmacyCreate, db: Session = Depends(get_db)):
    return pharmacy_services.create_pharmacy(db, pharmacy)


# PUT /pharmacies/{pharmacy_id} : modifier une pharmacie.
@router.put("/{pharmacy_id}", response_model=PharmacyItem)
def update_pharmacy(
    pharmacy_id: int,
    pharmacy: PharmacyUpdate,
    db: Session = Depends(get_db),
):
    return pharmacy_services.update_pharmacy(db, pharmacy_id, pharmacy)


# DELETE /pharmacies/{pharmacy_id} : supprimer une pharmacie.
@router.delete("/{pharmacy_id}")
def delete_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)):
    return pharmacy_services.delete_pharmacy(db, pharmacy_id)


# GET /pharmacies/{pharmacy_id}/users : utilisateurs liés à une pharmacie.
@router.get("/{pharmacy_id}/users", response_model=List[UserItem])
def get_pharmacy_users(pharmacy_id: int, db: Session = Depends(get_db)):
    return pharmacy_services.get_pharmacy_users(db, pharmacy_id)


# POST /pharmacies/{pharmacy_id}/users/{user_id} : lier un utilisateur.
@router.post("/{pharmacy_id}/users/{user_id}", response_model=PharmacyItem)
def attach_user(pharmacy_id: int, user_id: int, db: Session = Depends(get_db)):
    return pharmacy_services.attach_user(db, pharmacy_id, user_id)


# DELETE /pharmacies/{pharmacy_id}/users/{user_id} : retirer le lien.
@router.delete("/{pharmacy_id}/users/{user_id}", response_model=PharmacyItem)
def detach_user(pharmacy_id: int, user_id: int, db: Session = Depends(get_db)):
    return pharmacy_services.detach_user(db, pharmacy_id, user_id)
