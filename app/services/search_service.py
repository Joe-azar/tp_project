from app.utils.similarity_utils import cosine_similarity
from app.services.db_service import load_data
from app.models.document_model import Query
from sentence_transformers import SentenceTransformer

# Charger le modèle d'embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def search_documents(query: Query):
    query_embedding = model.encode(query.query).tolist()
    document_embeddings = load_data()  # Charger les données depuis le fichier JSON

    # Calculer la similarité cosinus pour chaque document
    results = []
    for doc in document_embeddings:
        similarity_score = cosine_similarity(query_embedding, doc["embedding"])
        results.append({
            "id": doc["id"],
            "text": doc["text"],
            "similarity_score": similarity_score
        })

    # Trier les résultats par similarité décroissante
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    return {"relevant_documents": results}
