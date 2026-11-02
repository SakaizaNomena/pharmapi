from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.database import Base
from src.app.models.association import user_pharmacy

if TYPE_CHECKING:
    from src.app.models.user_model import User


# TABLE : pharmacies
# ------------------
# Colonnes :
#   - id      : clé primaire, générée automatiquement
#   - name    : nom de la pharmacie (obligatoire)
#   - address : adresse de la pharmacie (obligatoire)
#   - city    : ville de la pharmacie (obligatoire)
#   - phone   : numéro de téléphone (obligatoire)
#
# Relation :
#   - users : liste des utilisateurs liés à cette pharmacie.
#     C'est l'inverse de User.pharmacies (back_populates).
class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    users: Mapped[list["User"]] = relationship(
        secondary=user_pharmacy,
        back_populates="pharmacies",
    )
