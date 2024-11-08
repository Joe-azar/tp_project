from pydantic import BaseModel
from typing import List

# Modèle pour la requête d'encodage de documents
class Documents(BaseModel):
    documents: List[str]

# Modèle pour la requête de recherche
class Query(BaseModel):
    query: str

# Modèle pour la réponse de recherche avec score de similarité
class RelevantDocument(BaseModel):
    id: int
    text: str
    similarity_score: float
