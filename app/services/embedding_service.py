from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import json

router = APIRouter()

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

class Documents(BaseModel):
    documents: list[str]

@router.post("/embed")
async def embed_documents(request: Documents):
    try:
        embeddings = [
            {"text": doc, "embedding": model.encode(doc).tolist()}
            for doc in request.documents
        ]

        # Stocker les résultats dans un fichier JSON
        with open("data/embeddings.json", "w") as f:
            json.dump(embeddings, f)

        return {"status": "success", "message": "Documents encodés avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'encodage : {e}")
