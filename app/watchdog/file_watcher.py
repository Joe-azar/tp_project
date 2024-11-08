import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from app.config import WATCHED_FOLDER
import sys
import os

# Ajouter le répertoire racine au chemin Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.config import WATCHED_FOLDER  # Importation correcte après modification


API_URL = "http://127.0.0.1:8000/encode_documents"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".txt"):
            process_file(event.src_path)

def process_file(file_path):
    print(f"New file detected: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    response = requests.post(API_URL, json={"documents": lines})
    if response.status_code == 200:
        print("File processed successfully:", response.json())
    else:
        print("Error processing file:", response.status_code, response.text)

if __name__ == "__main__":
    os.makedirs(WATCHED_FOLDER, exist_ok=True)
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()

    print(f"Watching folder: {WATCHED_FOLDER}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
