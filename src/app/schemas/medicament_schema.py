from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Champs communs à la création et à la lecture d'un médicament.
class MedicamentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: float = Field(..., ge=0)
    stock: int = Field(default=0, ge=0)
    pharmacy_id: int


# Données reçues pour créer un médicament (pas d'id).
class MedicamentCreate(MedicamentBase):
    pass


# Données reçues pour modifier un médicament.
# Tous les champs sont optionnels : on ne modifie que ceux envoyés.
class MedicamentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)
    pharmacy_id: Optional[int] = None


# Données renvoyées par l'API pour un médicament.
class MedicamentItem(MedicamentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
