import requests

def test_embed():
    url = "http://localhost:8000/embed"
    payload = {"documents": ["Texte exemple 1", "Texte exemple 2"]}
    response = requests.post(url, json=payload)
    print("Test Embed Response:", response.json())

def test_search():
    url = "http://localhost:8000/search"
    payload = {"query": "Texte exemple"}
    response = requests.post(url, json=payload)
    print("Test Search Response:", response.json())

if __name__ == "__main__":
    test_embed()
    test_search()
