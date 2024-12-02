from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.utils.cosine_similarity import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


router = APIRouter()

class Query(BaseModel):
    query: str
EMBEDDINGS_FILE = Path("data") / "embeddings.json"

@router.post("/search")
async def search_documents(request: Query):
    try:
        # Charger les embeddings depuis le fichier JSON
        if not EMBEDDINGS_FILE.exists():
            raise HTTPException(status_code=404, detail="Le fichier d'embeddings est introuvable.")

        with open(EMBEDDINGS_FILE, "r") as f:
            document_embeddings = json.load(f)

        # Vérifier que les embeddings sont valides
        if not document_embeddings:
            raise HTTPException(status_code=400, detail="Aucun embedding disponible pour la recherche.")

        # Encoder la requête
        query_embedding = model.encode(request.query).tolist()

        # Calculer les similarités cosinus
        results = []
        for doc in document_embeddings:
            similarity = cosine_similarity(query_embedding, doc["embedding"])
            results.append({
                "text": doc["text"],
                "similarity_score": similarity
            })

        # Trier les résultats par similarité décroissante
        results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

        return {"relevant_documents": results[:5]}  # Limite à 5 résultats
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier d'embeddings introuvable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche : {e}")
