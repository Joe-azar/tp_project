import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

class WatchdogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".txt"):
            print(f"Nouveau fichier détecté : {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        # Appeler le service d'encodage
        url = "http://localhost:8000/api/embed"
        payload = {"documents": lines}
        try:
            response = requests.post(url, json=payload)
            print("Réponse de l'API :", response.json())
        except Exception as e:
            print(f"Erreur API : {e}")

if __name__ == "__main__":
    folder_to_watch = "./data"
    observer = Observer()
    event_handler = WatchdogHandler()

    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print(f"Surveillance du dossier : {folder_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
