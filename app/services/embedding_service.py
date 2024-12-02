from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import json
import requests

# Définir les chemins pour les données
DATA_DIR = Path("data")
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
router = APIRouter()

# Initialisation du modèle
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

class Documents(BaseModel):
    documents: list[str]

@router.post("/embed")
async def embed_documents(request: Documents):
    try:
        # Charger les données existantes si elles existent
        try:
            if EMBEDDINGS_FILE.exists():
                with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                    existing_embeddings = json.load(f)
            else:
                existing_embeddings = []
        except (json.JSONDecodeError, IOError) as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors du chargement des embeddings existants : {e}")

        # Générer les nouveaux embeddings
        new_embeddings = [
            {"text": doc, "embedding": model.encode(doc).tolist()}
            for doc in request.documents
        ]

        # Fusionner les embeddings existants avec les nouveaux
        merged_embeddings = existing_embeddings + new_embeddings

        # Sauvegarder les embeddings mis à jour
        try:
            with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(merged_embeddings, f, indent=4)
        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de l'écriture des embeddings : {e}")

        # Appeler le service /insert pour stocker les données dans la base
        response = requests.post("http://127.0.0.1:8000/api/insert", json={"records": new_embeddings})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Erreur API /insert : {response.json()}")

        return {"status": "success", "message": "Documents encodés et insérés avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur générale : {e}")
