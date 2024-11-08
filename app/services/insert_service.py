from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter()

class Data(BaseModel):
    records: list[dict]

@router.post("/insert")
async def insert_in_db(data: Data):
    try:
        # Simuler l'insertion en écrivant dans un fichier JSON
        with open("data/database.json", "w") as f:
            json.dump(data.records, f)

        return {"status": "success", "message": "Données insérées avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'insertion : {e}")
