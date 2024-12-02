from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.embedding_service import router as embedding_router
from app.services.search_service import router as search_router
from app.services.insert_service import router as insert_router
import os

app = FastAPI(
    title="Embedding and Search API",
    description="API permettant l'encodage, l'insertion et la recherche de documents à l'aide d'embeddings.",
    version="1.0.0",
    contact={
        "name": "Support API",
        "email": "support@example.com",
    },
)

# Ajouter le middleware CORS si l'API doit être accessible depuis un frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Changez "*" par les origines spécifiques si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes des services
app.include_router(embedding_router, prefix="/api", tags=["Embedding"])
app.include_router(search_router, prefix="/api", tags=["Search"])
app.include_router(insert_router, prefix="/api", tags=["Insert"])

# Vérification des fichiers nécessaires au démarrage
@app.on_event("startup")
async def startup_event():
    required_files = ["data/embeddings.json", "data/database.json"]
    for file_path in required_files:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")  # Initialiser le fichier comme une liste vide
            print(f"Fichier {file_path} initialisé.")

# Endpoint racine
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenue dans l'API Embedding and Search"}
