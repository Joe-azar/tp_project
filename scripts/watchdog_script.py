import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

class WatchdogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".txt"):
            print(f"Nouveau fichier détecté : {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, file_path: str):
        try:
            # Lire le fichier et extraire les lignes non vides
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]

            # Vérifier que le fichier contient des données
            if not lines:
                print(f"Fichier vide ou mal formé : {file_path}")
                return

            # Appeler le service d'encodage
            url = "http://localhost:8000/api/embed"
            payload = {"documents": lines}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Réponse de l'API :", response.json())
        except FileNotFoundError:
            print(f"Fichier introuvable : {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur API : {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    folder_to_watch = Path("./data")
    if not folder_to_watch.exists():
        print(f"Dossier {folder_to_watch} introuvable.")
        exit(1)

    observer = Observer()
    event_handler = WatchdogHandler()

    observer.schedule(event_handler, str(folder_to_watch), recursive=False)
    observer.start()
    print(f"Surveillance du dossier : {folder_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
