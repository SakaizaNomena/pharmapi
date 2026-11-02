from pydantic import BaseModel


# Réponse générique pour les opérations qui ne renvoient pas de ressource
# (suppressions, déconnexion, etc.).
class MessageResponse(BaseModel):
    message: str
