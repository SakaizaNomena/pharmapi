from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.models.auth_token_model import AuthToken
from src.app.models.user_model import User

# HTTPBearer lit le header "Authorization: Bearer <token>".
# auto_error=False nous permet de renvoyer notre propre erreur 401.
bearer_scheme = HTTPBearer(auto_error=False)


# Dépendance : récupère le token envoyé par le client et vérifie qu'il existe.
def get_current_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthToken:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant : connectez-vous avec /auth/login",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_token = (
        db.query(AuthToken)
        .filter(AuthToken.token == credentials.credentials)
        .first()
    )
    if auth_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_token


# Dépendance : renvoie l'utilisateur connecté.
# C'est elle qu'on ajoute aux routers pour protéger les endpoints.
def get_current_user(
    auth_token: AuthToken = Depends(get_current_token),
) -> User:
    return auth_token.user
