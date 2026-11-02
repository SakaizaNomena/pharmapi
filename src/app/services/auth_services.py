import secrets

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.models.auth_token_model import AuthToken
from src.app.models.user_model import User
from src.app.schemas.auth_schema import LoginRequest, RegisterRequest


# Crée un token aléatoire et le sauvegarde en base pour cet utilisateur.
def create_token(db: Session, user: User) -> AuthToken:
    auth_token = AuthToken(
        token=secrets.token_urlsafe(32),
        user_id=user.id,
    )
    db.add(auth_token)
    db.commit()
    db.refresh(auth_token)
    return auth_token


# INSCRIPTION : vérifie que l'email est libre, crée l'utilisateur,
# puis le connecte directement en renvoyant un token.
def register(db: Session, data: RegisterRequest) -> AuthToken:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé",
        )

    user = User(name=data.name, email=data.email)
    db.add(user)
    db.commit()
    db.refresh(user)

    return create_token(db, user)


# CONNEXION : pas de mot de passe.
# On vérifie simplement que l'email correspond à un utilisateur existant,
# puis on génère un token.
def login(db: Session, data: LoginRequest) -> AuthToken:
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email non reconnu. Inscrivez-vous avec /auth/register",
        )

    return create_token(db, user)


# DÉCONNEXION : supprime le token utilisé.
def logout(db: Session, auth_token: AuthToken) -> dict:
    db.delete(auth_token)
    db.commit()
    return {"message": "Déconnecté avec succès"}
