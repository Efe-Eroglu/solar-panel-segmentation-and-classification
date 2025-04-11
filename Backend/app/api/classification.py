from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.classifier import predict_class
from app.schemas.predict import PredictionResponse
import shutil
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/predict-class", response_model=PredictionResponse)
async def classify_image(file: UploadFile = File(...)):
    try:
        # Geçici dosya kaydet
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Tahmini al
        prediction = predict_class(file_path)

        return PredictionResponse(
            predicted_class=prediction["class"],
            confidence=prediction["confidence"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
