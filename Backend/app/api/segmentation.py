from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.segmenter import segment_image
from app.schemas.predict import SegmentationResponse
import shutil
import uuid
import os
import logging
import traceback

# Logger ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/segment-image", response_model=SegmentationResponse)
async def segment_uploaded_image(file: UploadFile = File(...)):
    try:
        logger.info(f"Segmentation request received for file: {file.filename}")
        
        if not file:
            logger.error("No file uploaded")
            raise HTTPException(status_code=400, detail="Dosya yüklenemedi")
        
        # Izin verilen uzantıları kontrol et
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png"]:
            logger.error(f"Invalid file type: {file_ext}")
            raise HTTPException(status_code=400, detail="Sadece JPG, JPEG ve PNG dosya formatları kabul edilir")
        
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        logger.info(f"Saving file to: {file_path}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved successfully, processing for segmentation")
        
        result = segment_image(file_path)
        
        logger.info("Segmentation completed successfully")
        
        return SegmentationResponse(
            mask_base64=result["mask_base64"],
            description="Segmentation completed successfully"
        )

    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error in segmentation process: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        file.file.close()
