from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.models.medicament_model import Medicament
from src.app.models.pharmacy_model import Pharmacy
from src.app.models.user_model import User
from src.app.schemas.pharmacy_schema import PharmacyCreate, PharmacyUpdate


# READ : récupérer toutes les pharmacies.
def get_all_pharmacies(db: Session) -> List[Pharmacy]:
    return db.query(Pharmacy).all()


# READ : récupérer une pharmacie par son id.
def get_pharmacy(db: Session, pharmacy_id: int) -> Pharmacy:
    pharmacy = db.get(Pharmacy, pharmacy_id)
    if pharmacy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacie introuvable",
        )
    return pharmacy


# CREATE : créer une pharmacie.
def create_pharmacy(db: Session, pharmacy_data: PharmacyCreate) -> Pharmacy:
    pharmacy = Pharmacy(**pharmacy_data.model_dump())
    db.add(pharmacy)
    db.commit()
    db.refresh(pharmacy)
    return pharmacy


# UPDATE : modifier une pharmacie.
def update_pharmacy(
    db: Session,
    pharmacy_id: int,
    pharmacy_data: PharmacyUpdate,
) -> Pharmacy:
    pharmacy = get_pharmacy(db, pharmacy_id)

    # On ne modifie que les champs envoyés par le client.
    updates = pharmacy_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(pharmacy, field, value)

    db.commit()
    db.refresh(pharmacy)
    return pharmacy


# DELETE : supprimer une pharmacie.
def delete_pharmacy(db: Session, pharmacy_id: int) -> dict:
    pharmacy = get_pharmacy(db, pharmacy_id)
    db.delete(pharmacy)
    db.commit()
    return {"message": "Pharmacie supprimée"}


# READ : lister les utilisateurs d'une pharmacie.
def get_pharmacy_users(db: Session, pharmacy_id: int) -> List[User]:
    pharmacy = get_pharmacy(db, pharmacy_id)
    return pharmacy.users


# READ : lister les médicaments d'une pharmacie.
def get_pharmacy_medicaments(db: Session, pharmacy_id: int) -> List[Medicament]:
    pharmacy = get_pharmacy(db, pharmacy_id)
    return pharmacy.medicaments


# CREATE (relation) : ajouter un utilisateur à une pharmacie.
def attach_user(db: Session, pharmacy_id: int, user_id: int) -> Pharmacy:
    pharmacy = get_pharmacy(db, pharmacy_id)
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable",
        )

    # On évite les doublons dans la table d'association.
    if user not in pharmacy.users:
        pharmacy.users.append(user)
        db.commit()
        db.refresh(pharmacy)

    return pharmacy


# DELETE (relation) : retirer un utilisateur d'une pharmacie.
def detach_user(db: Session, pharmacy_id: int, user_id: int) -> Pharmacy:
    pharmacy = get_pharmacy(db, pharmacy_id)
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable",
        )

    if user in pharmacy.users:
        pharmacy.users.remove(user)
        db.commit()
        db.refresh(pharmacy)

    return pharmacy
