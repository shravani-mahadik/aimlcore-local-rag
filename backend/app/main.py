from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.search import router as search_router
from backend.app.api.chat import router as chat_router
from backend.app.api.documents import router as documents_router


app = FastAPI(
    title="AIMLCore Local Knowledge Assistant",
    description="Local RAG Knowledge Assistant API",
    version="1.0.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# API ROUTERS
# ==========================================

app.include_router(search_router)
app.include_router(chat_router)
app.include_router(documents_router)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():

    return {
        "message": "AIMLCore Local Knowledge Assistant API",
        "status": "running"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/system/health")
def health_check():

    return {
        "status": "healthy"
    }