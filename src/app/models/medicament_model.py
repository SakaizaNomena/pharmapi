from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.database import Base

if TYPE_CHECKING:
    from src.app.models.pharmacy_model import Pharmacy


# TABLE : medicaments
# -------------------
# Colonnes :
#   - id          : clé primaire
#   - name        : nom du médicament (obligatoire)
#   - description : description libre (facultative)
#   - price       : prix unitaire (obligatoire, >= 0)
#   - stock       : quantité disponible (obligatoire, >= 0)
#   - pharmacy_id : pharmacie qui vend ce médicament (clé étrangère)
#
# Relation :
#   - pharmacy : relation MANY-TO-ONE (plusieurs-à-un).
#     Plusieurs médicaments appartiennent à une seule pharmacie.
#     C'est l'inverse de Pharmacy.medicaments.
class Medicament(Base):
    __tablename__ = "medicaments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pharmacy_id: Mapped[int] = mapped_column(
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    pharmacy: Mapped["Pharmacy"] = relationship(back_populates="medicaments")
