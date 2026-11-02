from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.models.pharmacy_model import Pharmacy
from src.app.models.user_model import User
from src.app.schemas.user_schema import UserCreate, UserUpdate


# READ : récupérer tous les utilisateurs.
def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


# READ : récupérer un utilisateur par son id.
def get_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable",
        )
    return user


# CREATE : créer un utilisateur.
def create_user(db: Session, user_data: UserCreate) -> User:
    # On vérifie que l'email n'est pas déjà utilisé.
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé",
        )

    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# UPDATE : modifier un utilisateur.
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = get_user(db, user_id)

    # exclude_unset=True : on ne récupère que les champs réellement envoyés.
    updates = user_data.model_dump(exclude_unset=True)

    # Si l'email change, on vérifie qu'il n'appartient pas à un autre utilisateur.
    if "email" in updates:
        existing_user = (
            db.query(User)
            .filter(User.email == updates["email"], User.id != user_id)
            .first()
        )
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé",
            )

    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# DELETE : supprimer un utilisateur.
def delete_user(db: Session, user_id: int) -> dict:
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé"}


# READ : lister les pharmacies d'un utilisateur.
def get_user_pharmacies(db: Session, user_id: int) -> List[Pharmacy]:
    user = get_user(db, user_id)
    return user.pharmacies


# CREATE (relation) : ajouter une pharmacie à un utilisateur.
def attach_pharmacy(db: Session, user_id: int, pharmacy_id: int) -> User:
    user = get_user(db, user_id)
    pharmacy = db.get(Pharmacy, pharmacy_id)
    if pharmacy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacie introuvable",
        )

    # On évite les doublons dans la table d'association.
    if pharmacy not in user.pharmacies:
        user.pharmacies.append(pharmacy)
        db.commit()
        db.refresh(user)

    return user


# DELETE (relation) : retirer une pharmacie d'un utilisateur.
def detach_pharmacy(db: Session, user_id: int, pharmacy_id: int) -> User:
    user = get_user(db, user_id)
    pharmacy = db.get(Pharmacy, pharmacy_id)
    if pharmacy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacie introuvable",
        )

    if pharmacy in user.pharmacies:
        user.pharmacies.remove(pharmacy)
        db.commit()
        db.refresh(user)

    return user
