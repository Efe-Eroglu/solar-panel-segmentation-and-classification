from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.classifier import predict_class
from app.schemas.predict import PredictionResponse
import shutil
import uuid
import os
import logging
import traceback
import numpy as np

# Logger ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Model sınıf adları ve frontend sınıf adları eşleştirmesi
CLASS_NAME_MAP = {
    "clean": "normal",
    "bird-drop": "bird-drop",
    "dusty": "dusty",
    "electrical-damage": "electrical-damage",
    "physical-damage": "faulty",
    "snow-covered": "snow-covered"
}

@router.post("/predict-class")
async def classify_image(file: UploadFile = File(...)):
    try:
        logger.info(f"Classification request received for file: {file.filename}")
        
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
        
        logger.info(f"File saved successfully, processing for classification")
        
        # Tahmin yap (doğrudan byte olarak gönder)
        prediction = predict_class(img_bytes=file_bytes)
        
        logger.info(f"Classification result: {prediction}")
        
        # Frontend'in beklediği formata dönüştür
        # Tüm olasılıkları al
        probabilities = prediction["all_probabilities"]
        class_names = list(probabilities.keys())
        probs_values = list(probabilities.values())
        
        # Olasılıkları normalize et (toplamları 1 olacak şekilde)
        probs_sum = sum(probs_values)
        if probs_sum > 0:
            normalized_probs = [p / probs_sum for p in probs_values]
        else:
            normalized_probs = probs_values  # Toplam 0 ise normalizasyon yapma
        
        # Tüm sınıfları olasılık sırasına göre sırala (normalize edilmiş değerler kullanarak)
        sorted_indices = np.argsort(normalized_probs)[::-1]  # En yüksek olasılıktan en düşüğe
        
        # Sınıf adlarını frontend için düzgün formata dönüştür ve normalize et
        frontend_probabilities = {}
        for i, (backend_class, probability) in enumerate(zip(class_names, probs_values)):
            # Frontend sınıf adını bul
            frontend_class = CLASS_NAME_MAP.get(backend_class.lower(), backend_class)
            # Normalize edilmiş değeri kullan
            frontend_probabilities[frontend_class] = float(normalized_probs[i])
        
        # En yüksek tahmin için doğru frontend sınıf adını kullan
        top_backend_class = class_names[sorted_indices[0]]
        top_frontend_class = CLASS_NAME_MAP.get(top_backend_class.lower(), top_backend_class)
        
        # Sonuç formatını oluştur - TÜM sınıfları dahil et, normalize edilmiş değerlerle
        result = {
            "predictions": [
                {
                    "class": class_names[i].capitalize(),
                    "confidence": float(normalized_probs[i])
                }
                for i in sorted_indices  # Tüm indeksleri kullan
            ],
            "predicted_class": top_frontend_class,
            "confidence": float(normalized_probs[sorted_indices[0]]),
            "all_probabilities": frontend_probabilities
        }
        
        return result
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error during classification: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        if file:
            await file.close() 