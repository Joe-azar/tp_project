import subprocess
import threading
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import requests

# URL de l'API
API_URL_SEARCH = "http://127.0.0.1:8000/api/search"
DATA_FOLDER = "./data"

# Fonction pour lancer Uvicorn
def start_uvicorn():
    """Lancer le serveur FastAPI avec Uvicorn."""
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

# Fonction pour lancer Watchdog
def start_watchdog():
    """Lancer le script Watchdog pour surveiller les fichiers .txt."""
    subprocess.run(["python", "scripts/watchdog_script.py"])

def wait_for_api():
    """Attendre que l'API soit opérationnelle."""
    url = "http://127.0.0.1:8000/docs"
    for _ in range(10):  # Essayer 10 fois
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("API disponible.")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    raise Exception("L'API n'est pas disponible après 10 secondes.")

# Fonction pour lancer l'interface graphique
def start_gui():
    """Interface graphique avec Tkinter."""
    def insert_files():
        files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        if not files:
            return
        
        for file in files:
            filename = os.path.basename(file)
            destination = os.path.join(DATA_FOLDER, filename)
            os.makedirs(DATA_FOLDER, exist_ok=True)
            try:
                with open(file, "r", encoding="utf-8") as src, open(destination, "w", encoding="utf-8") as dest:
                    dest.write(src.read())
                messagebox.showinfo("Succès", f"Fichier '{filename}' déposé avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'insertion : {e}")

    def search_query():
        query = search_entry.get().strip()
        if not query:
            messagebox.showwarning("Attention", "Veuillez saisir un mot ou une phrase à rechercher.")
            return

        try:
            response = requests.post(API_URL_SEARCH, json={"query": query})
            if response.status_code == 200:
                results = response.json()["relevant_documents"]
                if results:
                    result_text = "\n\n".join([f"{doc['text']} (Score: {doc['similarity_score']:.2f})" for doc in results])
                else:
                    result_text = "Aucun document pertinent trouvé."
                
                messagebox.showinfo("Résultats de la recherche", result_text)
            else:
                messagebox.showerror("Erreur", f"Erreur API : {response.status_code}\n{response.json()}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    root = tk.Tk()
    root.title("Embedding & Search Application")

    # Section Insertion
    insert_frame = tk.LabelFrame(root, text="Insertion de fichiers", padx=10, pady=10)
    insert_frame.pack(fill="x", padx=10, pady=5)

    insert_button = tk.Button(insert_frame, text="Déposer des fichiers .txt", command=insert_files)
    insert_button.pack(fill="x", pady=5)

    # Section Recherche
    search_frame = tk.LabelFrame(root, text="Recherche de documents", padx=10, pady=10)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_label = tk.Label(search_frame, text="Entrez un mot ou une phrase :")
    search_label.pack(anchor="w", pady=5)

    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(fill="x", pady=5)

    search_button = tk.Button(search_frame, text="Rechercher", command=search_query)
    search_button.pack(fill="x", pady=5)

    root.mainloop()

# Fonction pour exécuter tous les services
def run_all_services():
    """Lancer tous les services nécessaires."""
    # Démarrer Uvicorn pour FastAPI
    uvicorn_thread = threading.Thread(target=start_uvicorn)
    uvicorn_thread.start()

    # Attendre que l'API soit en ligne
    wait_for_api()

    # Démarrer le script Watchdog
    watchdog_thread = threading.Thread(target=start_watchdog)
    watchdog_thread.start()

    # Lancer l'interface graphique
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()

    # Attendre que les threads se terminent (facultatif)
    uvicorn_thread.join()
    watchdog_thread.join()
    gui_thread.join()

if __name__ == "__main__":
    print("Lancement de tous les services...")
    run_all_services()
