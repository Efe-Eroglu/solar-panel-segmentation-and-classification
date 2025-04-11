from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import classification, segmentation
from app.core.model_registry import ModelRegistry

app = FastAPI(
    title="Solar Panel Fault Detection API",
    description="Sınıflandırma ve segmentasyon işlemleri için REST API",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_all_models():
    ModelRegistry.load_models()

app.include_router(classification.router, prefix="/api", tags=["Classification"])
app.include_router(segmentation.router, prefix="/api", tags=["Segmentation"])

@app.get("/")
def read_root():
    return {"message": "API is up and running!"}
