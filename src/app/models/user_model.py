from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.database import Base
from src.app.models.association import user_pharmacy

if TYPE_CHECKING:
    from src.app.models.auth_token_model import AuthToken
    from src.app.models.pharmacy_model import Pharmacy


# TABLE : users
# -------------
# Colonnes :
#   - id    : clé primaire, générée automatiquement
#   - name  : nom de l'utilisateur (obligatoire)
#   - email : email unique (un email ne peut pas être utilisé deux fois)
#
# Relation :
#   - pharmacies : liste des pharmacies liées à cet utilisateur.
#     La relation passe par la table d'association user_pharmacy.
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    pharmacies: Mapped[list["Pharmacy"]] = relationship(
        secondary=user_pharmacy,
        back_populates="users",
    )

    # Tokens de connexion liés à cet utilisateur.
    # Si l'utilisateur est supprimé, ses tokens sont supprimés aussi.
    tokens: Mapped[list["AuthToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
