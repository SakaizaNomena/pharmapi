from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.core.security import get_current_user
from src.app.schemas.common_schema import MessageResponse
from src.app.schemas.medicament_schema import (
    MedicamentCreate,
    MedicamentItem,
    MedicamentUpdate,
)
from src.app.services import medicament_services

# Tag "medicaments".
# dependencies=[Depends(get_current_user)] protège TOUTES les routes :
# sans token valide, l'API renvoie 401 Unauthorized.
router = APIRouter(
    prefix="/medicaments",
    tags=["medicaments"],
    dependencies=[Depends(get_current_user)],
)


# GET /medicaments/ : liste des médicaments.
# Filtre optionnel : /medicaments/?pharmacy_id=1
@router.get("/", response_model=List[MedicamentItem])
def get_medicaments(
    pharmacy_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return medicament_services.get_all_medicaments(db, pharmacy_id)


# GET /medicaments/{medicament_id} : un médicament par son id.
@router.get("/{medicament_id}", response_model=MedicamentItem)
def get_medicament(medicament_id: int, db: Session = Depends(get_db)):
    return medicament_services.get_medicament(db, medicament_id)


# POST /medicaments/ : créer un médicament.
@router.post("/", response_model=MedicamentItem, status_code=201)
def create_medicament(
    medicament: MedicamentCreate,
    db: Session = Depends(get_db),
):
    return medicament_services.create_medicament(db, medicament)


# PUT /medicaments/{medicament_id} : modifier un médicament.
@router.put("/{medicament_id}", response_model=MedicamentItem)
def update_medicament(
    medicament_id: int,
    medicament: MedicamentUpdate,
    db: Session = Depends(get_db),
):
    return medicament_services.update_medicament(
        db,
        medicament_id,
        medicament,
    )


# DELETE /medicaments/{medicament_id} : supprimer un médicament.
@router.delete("/{medicament_id}", response_model=MessageResponse)
def delete_medicament(medicament_id: int, db: Session = Depends(get_db)):
    return medicament_services.delete_medicament(db, medicament_id)
