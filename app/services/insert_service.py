from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

class Data(BaseModel):
    records: list[dict]
# Fichier JSON pour la base de données
DB_FILE = Path("data") / "database.json"

@router.post("/insert")
async def insert_in_db(data: Data):
    try:
        # Vérifier si le fichier existe, sinon l'initialiser avec une liste vide
        if not DB_FILE.exists():
            DB_FILE.write_text(json.dumps([]))

        # Charger les données existantes
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                # Réinitialiser le fichier s'il est corrompu
                existing_data = []
                DB_FILE.write_text(json.dumps([]))

        # Vérifier que les données contiennent les bonnes clés
        for record in data.records:
            if "text" not in record or "embedding" not in record:
                raise HTTPException(status_code=400, detail="Chaque enregistrement doit contenir 'text' et 'embedding'.")

        # Ajouter les nouveaux enregistrements
        existing_data.extend(data.records)

        # Sauvegarder les données mises à jour
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

        return {"status": "success", "message": "Données insérées avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'insertion : {e}")
