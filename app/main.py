from fastapi import FastAPI
from app.services.embedding_service import router as embedding_router
from app.services.search_service import router as search_router
from app.services.insert_service import router as insert_router
import os
import json

app = FastAPI(title="Embedding and Search API")

# Fichiers nécessaires
DATA_FOLDER = "data"
EMBEDDINGS_FILE = os.path.join(DATA_FOLDER, "embeddings.json")
DATABASE_FILE = os.path.join(DATA_FOLDER, "database.json")


@app.on_event("startup")
async def startup_event():
    """Initialisation des fichiers nécessaires au démarrage de l'application."""
    os.makedirs(DATA_FOLDER, exist_ok=True)  # Créer le dossier 'data' s'il n'existe pas

    # Vérifier et initialiser embeddings.json
    if not os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)  # Initialiser avec une liste vide
        print(f"{EMBEDDINGS_FILE} initialisé avec une liste vide.")

    # Vérifier et initialiser database.json
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)  # Initialiser avec une liste vide
        print(f"{DATABASE_FILE} initialisé avec une liste vide.")


# Inclure les routes des services
app.include_router(embedding_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(insert_router, prefix="/api")
