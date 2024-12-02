import json
from typing import Any, Dict

def read_json(file_path: str) -> Any:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
    except json.JSONDecodeError:
        raise ValueError(f"Le fichier {file_path} n'est pas un JSON valide.")

def write_json(file_path: str, data: Any) -> None:
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise IOError(f"Erreur lors de l'écriture dans le fichier {file_path} : {e}")
