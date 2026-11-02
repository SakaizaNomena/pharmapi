from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.api.auth import router as auth_router
from src.app.api.medicaments import router as medicaments_router
from src.app.api.pharmacies import router as pharmacies_router
from src.app.api.users import router as users_router
from src.app.core.database import Base, engine

# On importe les modèles pour que SQLAlchemy les enregistre avant create_all().
from src.app.models import AuthToken, Medicament, Pharmacy, User  # noqa: F401


# Au démarrage de l'application, on crée les tables si elles n'existent pas.
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Fast API - Users & Pharmacies",
    description="Pharmapi : SQLite + SQLAlchemy + relation vendeur/post.",
    lifespan=lifespan,
)

# Tags d'API : "auth", "users", "pharmacies" et "medicaments" (visibles dans /docs).
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(pharmacies_router)
app.include_router(medicaments_router)
