# On importe les modèles ici pour que SQLAlchemy les connaisse
# avant l'appel à Base.metadata.create_all().
from src.app.models.pharmacy_model import Pharmacy
from src.app.models.user_model import User

__all__ = ["User", "Pharmacy"]
