import json

# Fonction pour enregistrer les embeddings dans un fichier JSON
def save_embeddings_to_json(encoded_data, file_path="app/data/document_embeddings.json"):
    with open(file_path, "w") as f:
        json.dump(encoded_data, f)

# Fonction pour charger les embeddings depuis un fichier JSON
def load_embeddings_from_json(file_path="app/data/document_embeddings.json"):
    with open(file_path, "r") as f:
        return json.load(f)
