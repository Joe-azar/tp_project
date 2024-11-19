import subprocess
import threading
import time
import os

def start_uvicorn():
    """Lancer le serveur FastAPI avec Uvicorn."""
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_watchdog():
    """Lancer le script Watchdog pour surveiller les fichiers .txt."""
    subprocess.run(["python", "scripts/watchdog_script.py"])

def run_all_services():
    """Lancer tous les services nécessaires."""
    # Démarrer Uvicorn pour FastAPI
    uvicorn_thread = threading.Thread(target=start_uvicorn)
    uvicorn_thread.start()

    # Attendre un peu pour s'assurer que l'API est en ligne
    time.sleep(5)

    # Démarrer le script de surveillance
    watchdog_thread = threading.Thread(target=start_watchdog)
    watchdog_thread.start()

    # Attendre que les threads se terminent (facultatif, selon votre besoin)
    uvicorn_thread.join()
    watchdog_thread.join()

if __name__ == "__main__":
    print("Lancement de tous les services...")
    run_all_services()
