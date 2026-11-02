from pydantic import BaseModel, EmailStr, Field

from src.app.schemas.user_schema import UserItem


# Données pour s'inscrire : un nom + un email valide.
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


# Données pour se connecter : uniquement l'email (pas de mot de passe).
class LoginRequest(BaseModel):
    email: EmailStr


# Réponse renvoyée après register ou login.
# Le client doit garder access_token et l'envoyer dans le header :
#   Authorization: Bearer <access_token>
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserItem
