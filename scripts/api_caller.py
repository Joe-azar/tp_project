import requests

BASE_URL = "http://localhost:8000"

def test_embed(documents):
    url = f"{BASE_URL}/embed"
    payload = {"documents": documents}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Test Embed Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à /embed : {e}")

def test_search(query):
    url = f"{BASE_URL}/search"
    payload = {"query": query}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Test Search Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à /search : {e}")

if __name__ == "__main__":
    test_embed(["Texte exemple 1", "Texte exemple 2"])
    test_search("Texte exemple")
