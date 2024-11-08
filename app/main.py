from fastapi import FastAPI
from app.models.document_model import Documents, Query
from app.services.embedding_service import encode_documents
from app.services.search_service import search_documents

app = FastAPI()

# Route pour encoder les documents
@app.post("/encode_documents")
async def encode_docs(documents: Documents):
    return encode_documents(documents)

# Route pour rechercher des documents
@app.post("/search_documents")
async def search_docs(query: Query):
    return search_documents(query)
