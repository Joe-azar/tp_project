from fastapi import FastAPI
from services.embedding_service import router as embedding_router
from services.search_service import router as search_router
from services.insert_service import router as insert_router

app = FastAPI(title="Embedding and Search API")

# Inclure les routes des services
app.include_router(embedding_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(insert_router, prefix="/api")
