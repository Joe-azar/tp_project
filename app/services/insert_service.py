from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

class Data(BaseModel):
    records: list[dict]

@router.post("/insert")
async def insert_in_db(data: Data):
    try:
        # Vérifier si le fichier database.json existe
        if not os.path.exists("data/database.json"):
            with open("data/database.json", "w") as f:
                json.dump([], f)

        # Charger les données existantes
        with open("data/database.json", "r") as f:
            existing_data = json.load(f)

        # Ajouter les nouveaux enregistrements
        existing_data.extend(data.records)

        # Sauvegarder dans database.json
        with open("data/database.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        return {"status": "success", "message": "Données insérées avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'insertion : {e}")
