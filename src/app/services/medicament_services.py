from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.models.medicament_model import Medicament
from src.app.models.pharmacy_model import Pharmacy
from src.app.schemas.medicament_schema import (
    MedicamentCreate,
    MedicamentUpdate,
)


# Vérifie qu'une pharmacie existe avant de créer/modifier un médicament.
def _get_pharmacy_or_404(db: Session, pharmacy_id: int) -> Pharmacy:
    pharmacy = db.get(Pharmacy, pharmacy_id)
    if pharmacy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacie introuvable",
        )
    return pharmacy


# READ : récupérer tous les médicaments.
# On peut filtrer avec ?pharmacy_id=1.
def get_all_medicaments(
    db: Session,
    pharmacy_id: Optional[int] = None,
) -> List[Medicament]:
    query = db.query(Medicament)
    if pharmacy_id is not None:
        query = query.filter(Medicament.pharmacy_id == pharmacy_id)
    return query.all()


# READ : récupérer un médicament par son id.
def get_medicament(db: Session, medicament_id: int) -> Medicament:
    medicament = db.get(Medicament, medicament_id)
    if medicament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médicament introuvable",
        )
    return medicament


# CREATE : créer un médicament lié à une pharmacie.
def create_medicament(
    db: Session,
    medicament_data: MedicamentCreate,
) -> Medicament:
    _get_pharmacy_or_404(db, medicament_data.pharmacy_id)

    medicament = Medicament(**medicament_data.model_dump())
    db.add(medicament)
    db.commit()
    db.refresh(medicament)
    return medicament


# UPDATE : modifier un médicament.
def update_medicament(
    db: Session,
    medicament_id: int,
    medicament_data: MedicamentUpdate,
) -> Medicament:
    medicament = get_medicament(db, medicament_id)
    updates = medicament_data.model_dump(exclude_unset=True)

    # Si on change la pharmacie, on vérifie qu'elle existe.
    if "pharmacy_id" in updates:
        _get_pharmacy_or_404(db, updates["pharmacy_id"])

    for field, value in updates.items():
        setattr(medicament, field, value)

    db.commit()
    db.refresh(medicament)
    return medicament


# DELETE : supprimer un médicament.
def delete_medicament(db: Session, medicament_id: int) -> dict:
    medicament = get_medicament(db, medicament_id)
    db.delete(medicament)
    db.commit()
    return {"message": "Médicament supprimé"}
