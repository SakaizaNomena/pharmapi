from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.app.schemas.pharmacy_schema import PharmacyItem


# Champs communs à la création et à la lecture d'un utilisateur.
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)


# Données reçues pour créer un utilisateur (pas d'id).
class UserCreate(UserBase):
    pass


# Données reçues pour modifier un utilisateur.
# Tous les champs sont optionnels : on ne modifie que ceux envoyés.
class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[str] = Field(default=None, min_length=5, max_length=255)


# Données renvoyées par l'API pour un utilisateur.
class UserItem(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Version détaillée : l'utilisateur + ses pharmacies.
class UserWithPharmacies(UserItem):
    pharmacies: List[PharmacyItem] = []
