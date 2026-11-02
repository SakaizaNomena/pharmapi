from sqlalchemy import Column, ForeignKey, Table

from src.app.core.database import Base

# TABLE D'ASSOCIATION : user_pharmacy
# ------------------------------------
# Cette table relie les utilisateurs et les pharmacies.
# C'est une relation MANY-TO-MANY (plusieurs-à-plusieurs) :
#   - un utilisateur peut être lié à plusieurs pharmacies
#   - une pharmacie peut être liée à plusieurs utilisateurs
#
# Elle ne contient que les deux clés étrangères :
#   - user_id     -> référence users.id
#   - pharmacy_id -> référence pharmacies.id
#
# La paire (user_id, pharmacy_id) est une clé primaire composée :
# on ne peut donc pas ajouter deux fois la même relation.
user_pharmacy = Table(
    "user_pharmacy",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "pharmacy_id",
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
