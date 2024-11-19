from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.utils.cosine_similarity import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/search")
async def search_documents(request: Query):
    try:
        # Charger les embeddings depuis le fichier JSON
        with open("data/embeddings.json", "r") as f:
            document_embeddings = json.load(f)

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

        return {"relevant_documents": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche : {e}")
