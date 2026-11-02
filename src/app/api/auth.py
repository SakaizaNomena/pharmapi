from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.core.security import get_current_token, get_current_user
from src.app.models.auth_token_model import AuthToken
from src.app.models.user_model import User
from src.app.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from src.app.schemas.common_schema import MessageResponse
from src.app.schemas.user_schema import UserItem
from src.app.services import auth_services

# Tag "auth" : routes publiques d'inscription/connexion + routes protégées.
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# POST /auth/register : inscription sans mot de passe.
# Crée l'utilisateur, vérifie que l'email est libre et renvoie un token.
@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    auth_token = auth_services.register(db, data)
    return TokenResponse(
        access_token=auth_token.token,
        user=auth_token.user,
    )


# POST /auth/login : connexion avec le seul email.
# Si l'email existe, renvoie un nouveau token.
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    auth_token = auth_services.login(db, data)
    return TokenResponse(
        access_token=auth_token.token,
        user=auth_token.user,
    )


# GET /auth/me : renvoie l'utilisateur actuellement connecté.
# Protégé : il faut envoyer le token.
@router.get("/me", response_model=UserItem)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# POST /auth/logout : supprime le token utilisé (déconnexion).
@router.post("/logout", response_model=MessageResponse)
def logout(
    auth_token: AuthToken = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    return auth_services.logout(db, auth_token)
