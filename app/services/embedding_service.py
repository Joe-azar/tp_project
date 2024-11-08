from app.utils.file_utils import save_embeddings_to_json
from app.models.document_model import Documents
from sentence_transformers import SentenceTransformer
import numpy as np

# Charger le modèle d'embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Fonction pour encoder et stocker les documents
def encode_documents(documents: Documents):
    encoded_data = []

    for index, text in enumerate(documents.documents):
        embedding = model.encode(text).tolist()
        encoded_data.append({
            "id": index,
            "text": text,
            "embedding": embedding
        })

    # Enregistrer les embeddings dans un fichier JSON
    save_embeddings_to_json(encoded_data)

    return {"status": "success", "message": "Documents encoded and stored successfully"}
