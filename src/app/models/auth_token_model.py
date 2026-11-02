from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.database import Base

if TYPE_CHECKING:
    from src.app.models.user_model import User


# TABLE : auth_tokens
# -------------------
# Cette table stocke les tokens de connexion.
#
# Fonctionnement (sans mot de passe) :
#   1. L'utilisateur s'inscrit ou se connecte avec son email.
#   2. Le serveur vérifie que l'email existe, puis génère un token aléatoire.
#   3. Ce token est stocké ici et renvoyé au client.
#   4. Le client envoie ce token dans le header : Authorization: Bearer <token>.
#   5. Grâce à ce token, on retrouve l'utilisateur courant.
#
# Colonnes :
#   - id         : clé primaire
#   - token      : token unique et aléatoire
#   - user_id    : utilisateur propriétaire du token (clé étrangère)
#   - created_at : date de création du token
#
# Relation :
#   - user : l'utilisateur associé à ce token.
class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    token: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="tokens")
