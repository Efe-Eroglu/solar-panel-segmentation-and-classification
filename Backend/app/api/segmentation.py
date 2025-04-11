from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.segmenter import segment_image
from app.schemas.predict import SegmentationResponse
import shutil
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/segment-image", response_model=SegmentationResponse)
async def segment_uploaded_image(file: UploadFile = File(...)):
    try:
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = segment_image(file_path)

        return SegmentationResponse(
            mask_base64=result["mask_base64"],
            description="Segmentation completed successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
