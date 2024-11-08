from app.services.db_service import insert_embeddings
from app.models.document_model import Documents
from sentence_transformers import SentenceTransformer

# Charger le modèle d'embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def encode_documents(documents: Documents):
    encoded_data = []

    for index, text in enumerate(documents.documents):
        embedding = model.encode(text).tolist()
        encoded_data.append({
            "id": index,
            "text": text,
            "embedding": embedding
        })

    # Insérer directement dans le fichier JSON
    return insert_embeddings(encoded_data)
