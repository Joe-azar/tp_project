import json
import os
from app.config import DATA_FILE

# Charger les données existantes depuis le fichier JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Enregistrer les données dans le fichier JSON
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Insérer de nouveaux embeddings
def insert_embeddings(embeddings):
    try:
        existing_data = load_data()  # Charger les données existantes
        existing_data.extend(embeddings)  # Ajouter les nouveaux embeddings
        save_data(existing_data)  # Sauvegarder les données mises à jour
        return {"status": "success", "message": f"{len(embeddings)} embeddings inserted successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
