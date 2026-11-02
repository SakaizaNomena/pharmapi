from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Champs communs à la création et à la lecture d'une pharmacie.
class PharmacyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    address: str = Field(..., min_length=2, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=5, max_length=30)


# Données reçues pour créer une pharmacie (pas d'id : il est généré par la base).
class PharmacyCreate(PharmacyBase):
    pass


# Données reçues pour modifier une pharmacie.
# Tous les champs sont optionnels : on ne modifie que ceux envoyés.
class PharmacyUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    address: Optional[str] = Field(default=None, min_length=2, max_length=255)
    city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, min_length=5, max_length=30)


# Données renvoyées par l'API pour une pharmacie.
# from_attributes=True permet de convertir directement un objet SQLAlchemy.
class PharmacyItem(PharmacyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
