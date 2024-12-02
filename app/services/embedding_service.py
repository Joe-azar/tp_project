from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import json
import requests  # Ajoutez requests pour faire un appel à /insert
import os

# Définir un chemin global pour les données
DATA_DIR = Path("data")
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
router = APIRouter()

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

class Documents(BaseModel):
    documents: list[str]

@router.post("/embed")
async def embed_documents(request: Documents):
    try:
        # Générer les embeddings
        embeddings = [
            {"text": doc, "embedding": model.encode(doc).tolist()}
            for doc in request.documents
        ]

        # Charger les données existantes si le fichier existe
        if EMBEDDINGS_FILE.exists():
            with open(EMBEDDINGS_FILE, "r") as f:
                existing_embeddings = json.load(f)
        else:
            existing_embeddings = []

        # Ajouter les nouveaux embeddings
        existing_embeddings.extend(embeddings)

        # Stocker les embeddings mis à jour
        with open(EMBEDDINGS_FILE, "w") as f:
            json.dump(existing_embeddings, f, indent=4)

        # Appeler le service /insert
        response = requests.post("http://127.0.0.1:8000/api/insert", json={"records": embeddings})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return {"status": "success", "message": "Documents encodés et insérés avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'encodage ou d'insertion : {e}")
