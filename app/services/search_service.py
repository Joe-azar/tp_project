from app.utils.file_utils import load_embeddings_from_json
from app.utils.similarity_utils import cosine_similarity
from app.models.document_model import Query, RelevantDocument
from sentence_transformers import SentenceTransformer

# Charger le modèle d'embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def search_documents(query: Query):
    # Encoder la requête
    query_embedding = model.encode(query.query).tolist()

    # Charger les embeddings des documents
    document_embeddings = load_embeddings_from_json()

    # Calculer la similarité cosinus pour chaque document
    results = []
    for doc in document_embeddings:
        similarity_score = cosine_similarity(query_embedding, doc["embedding"])
        results.append(RelevantDocument(id=doc["id"], text=doc["text"], similarity_score=similarity_score))

    # Trier les résultats par score décroissant
    results = sorted(results, key=lambda x: x.similarity_score, reverse=True)

    return {"relevant_documents": results}
