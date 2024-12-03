import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

router = APIRouter()

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
EMBEDDINGS_FILE = "data/embeddings.json"

class Documents(BaseModel):
    documents: list[str]

@router.post("/embed")
async def embed_documents(request: Documents):
    try:
        # Générer les embeddings pour les nouveaux documents
        new_embeddings = [
            {"text": doc, "embedding": model.encode(doc).tolist()}
            for doc in request.documents
        ]

        # Charger les embeddings existants (s'ils existent)
        if os.path.exists(EMBEDDINGS_FILE):
            with open(EMBEDDINGS_FILE, "r") as f:
                existing_embeddings = json.load(f)
        else:
            existing_embeddings = []

        # Ajouter les nouveaux embeddings aux existants
        existing_embeddings.extend(new_embeddings)

        # Sauvegarder tous les embeddings dans le fichier
        with open(EMBEDDINGS_FILE, "w") as f:
            json.dump(existing_embeddings, f, indent=4)

        return {"status": "success", "message": "Documents encodés et ajoutés avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'encodage : {e}")
