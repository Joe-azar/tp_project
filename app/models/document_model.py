from pydantic import BaseModel
from typing import List

# Modèle pour les documents à encoder
class Documents(BaseModel):
    documents: List[str]

# Modèle pour la requête utilisateur
class Query(BaseModel):
    query: str
