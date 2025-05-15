from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.predict import SegmentationResponse
import shutil
import uuid
import os
import logging
import traceback
import base64
from PIL import Image
import io
import numpy as np

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
        
        # Dosyayı oku
        file_bytes = await file.read()
        
        # Dosyayı kaydet
        with open(file_path, "wb") as buffer:
            buffer.write(file_bytes)
        
        logger.info(f"File saved successfully, processing for segmentation")
        
        # Geçici çözüm: Dummy segmentasyon
        # Gerçek segmentasyon kodu yerine sadece yüklenen görüntüyü döndür
        # ve boş bir maske oluştur
        
        # Dosyayı yeniden aç ve Base64'e çevir
        img = Image.open(file_path)
        
        # Overlay için orijinal resmi kullan
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        overlay_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Maske için siyah bir görüntü oluştur
        mask_img = Image.new('L', img.size, 0)  # Siyah maske
        mask_buffered = io.BytesIO()
        mask_img.save(mask_buffered, format="PNG")
        mask_base64 = base64.b64encode(mask_buffered.getvalue()).decode('utf-8')
        
        logger.info("Dummy segmentation completed successfully")
        
        return SegmentationResponse(
            mask_base64=mask_base64,
            overlay_base64=overlay_base64,
            description="Segmentasyon modülü şu anda bakım modunda. Gerçek sonuçlar yerine yüklenen görüntü gösterilmektedir."
        )

    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error in segmentation process: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        await file.close()
