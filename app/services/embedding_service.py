from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import json
import requests  # Ajoutez requests pour faire un appel à /insert

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

        # Stocker les embeddings dans embeddings.json
        with open("data/embeddings.json", "w") as f:
            json.dump(embeddings, f)

        # Envoyer les embeddings au service /insert
        response = requests.post("http://127.0.0.1:8000/api/insert", json={"records": embeddings})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return {"status": "success", "message": "Documents encodés et insérés avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'encodage ou d'insertion : {e}")
