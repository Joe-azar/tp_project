from fastapi import FastAPI
from app.models.document_model import Documents, Query
from app.services.embedding_service import encode_documents
from app.services.search_service import search_documents
from app.services.db_service import insert_embeddings

app = FastAPI()

@app.post("/encode_documents")
async def encode_docs(documents: Documents):
    return encode_documents(documents)

@app.post("/search_documents")
async def search_docs(query: Query):
    return search_documents(query)

@app.post("/insert_in_db")
async def insert_in_db(data: dict):
    return insert_embeddings(data["embeddings"])
