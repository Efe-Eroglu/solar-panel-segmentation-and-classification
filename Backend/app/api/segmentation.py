from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Path
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.schemas.predict import SegmentationResponse, SegmentationImageResponse
import shutil
import uuid
import os
import logging
import traceback
import base64
from PIL import Image
import io
import numpy as np
from typing import Optional

# Gerekli TensorFlow ve OpenCV kütüphanelerini import et
import tensorflow as tf
import cv2

# Model ve metrikleri tanımla
from tensorflow.keras.models import load_model

# Logger ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Model dosya yolu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../Backend
MODEL_PATH = os.path.join(BASE_DIR, "app", "model", "segmentation.h5")
logger.info(f"Model yolu: {MODEL_PATH}")

# --- 1. Özelleştirilmiş metrik & loss fonksiyonları ---
def iou_metric(y_true, y_pred):
    y_true = tf.cast(y_true > 0.5, tf.float32)
    y_pred = tf.cast(y_pred > 0.5, tf.float32)
    inter = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) - inter
    return (inter + 1e-7) / (union + 1e-7)

def dice_coef(y_true, y_pred):
    y_true = tf.cast(y_true > 0.5, tf.float32)
    y_pred = tf.cast(y_pred > 0.5, tf.float32)
    num = 2 * tf.reduce_sum(y_true * y_pred)
    den = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    return (num + 1e-7) / (den + 1e-7)

def combined_loss(y_true, y_pred):
    bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)
    return 0.5 * (1 - dice_coef(y_true, y_pred)) + 0.5 * bce

# Model değişkeni
segmentation_model = None

# Uygulama başlangıcında model yükleme
def load_segmentation_model():
    global segmentation_model
    try:
        logger.info(f"Model yükleniyor: {MODEL_PATH}")
        segmentation_model = load_model(
            MODEL_PATH,
            custom_objects={
                "iou_metric": iou_metric,
                "dice_coef": dice_coef,
                "combined_loss": combined_loss
            },
            compile=False
        )
        logger.info(f"Model başarıyla yüklendi: {MODEL_PATH}")
        return True
    except Exception as e:
        logger.error(f"Model yüklenirken hata: {str(e)}")
        raise RuntimeError(f"Model yüklenirken hata: {str(e)}")

# --- 5. Ön-işlem ve post-işlem fonksiyonları ---
def preprocess_image(image: Image.Image, target_size=(256,256)):
    image = image.convert("RGB").resize(target_size)
    arr = np.array(image)
    arr = tf.keras.applications.resnet50.preprocess_input(arr)
    return np.expand_dims(arr, axis=0)

def postprocess_mask(pred: np.ndarray, threshold=0.5):
    mask = pred.squeeze()
    mask = (mask > threshold).astype(np.uint8) * 255
    kernel = np.ones((3,3), np.uint8)
    closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return closed

# Görüntü segmentasyonu yapma fonksiyonu
def perform_segmentation(img: Image.Image):
    # Model yüklü değilse yükle
    global segmentation_model
    if segmentation_model is None:
        success = load_segmentation_model()
        if not success:
            raise RuntimeError("Segmentasyon modeli yüklenemedi")
    
    # Görüntüyü ön işleme tabi tut
    processed_img = preprocess_image(img)
    
    # Modeli çalıştır ve tahmini al
    logger.info("Model tahmin yapıyor...")
    prediction = segmentation_model.predict(processed_img)
    logger.info("Tahmin tamamlandı, sonuç işleniyor...")
    
    # Tahmini işle ve dön
    mask = postprocess_mask(prediction)
    logger.info("Maske oluşturuldu.")
    
    return mask

# Statik dosyaların sunulacağı URL
STATIC_URL = "/static/uploads"

# Doğrudan PNG resim döndüren endpoint
@router.post("/segment-image")
async def segment_uploaded_image(
    file: UploadFile = File(...),
    type: Optional[str] = Query("mask", description="Görüntü tipi (overlay veya mask)")
):
    try:
        logger.info(f"Direct image segmentation request received for file: {file.filename}")
        
        if not file:
            logger.error("No file uploaded")
            raise HTTPException(status_code=400, detail="Dosya yüklenemedi")
        
        # Izin verilen uzantıları kontrol et
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png"]:
            logger.error(f"Invalid file type: {file_ext}")
            raise HTTPException(status_code=400, detail="Sadece JPG, JPEG ve PNG dosya formatları kabul edilir")
        
        # Dosyayı oku
        file_bytes = await file.read()
        
        # Dosyayı işle
        img = Image.open(io.BytesIO(file_bytes))
        logger.info(f"Görüntü boyutu: {img.size}")
        
        # Segmentasyonu gerçekleştir
        try:
            # Gerçek segmentasyonu yap
            mask = perform_segmentation(img)
            logger.info("Segmentasyon başarıyla tamamlandı")
        except Exception as seg_err:
            logger.error(f"Segmentasyon hatası: {str(seg_err)}")
            raise HTTPException(status_code=500, detail=f"Segmentasyon hatası: {str(seg_err)}")
        
        # İstenilen resim tipine göre işlem yap
        output_buffer = io.BytesIO()
        
        if type == "mask":
            # Siyah-beyaz maske görüntüsünü oluştur ve kaydet
            mask_img = Image.fromarray(mask)
            mask_img.save(output_buffer, format="PNG")
            logger.info("Siyah-beyaz maske görüntüsü oluşturuldu")
        else:
            # Overlay oluştur (orjinal resim üzerine maske uygula)
            # Maske görüntüsünü oluştur
            mask_img = Image.fromarray(mask).convert("L")
            
            # Overlay için orijinal resim üzerine maske uygula
            img_array = np.array(img)
            # Kırmızı kanalı maskele
            img_array[:,:,0] = np.where(mask > 0, 255, img_array[:,:,0])
            # Mavi ve yeşil kanalları hafifçe koyulaştır
            img_array[:,:,1] = np.where(mask > 0, img_array[:,:,1] * 0.7, img_array[:,:,1])
            img_array[:,:,2] = np.where(mask > 0, img_array[:,:,2] * 0.7, img_array[:,:,2])
            
            # Overlay görüntüsünü oluştur ve kaydet
            overlay_img = Image.fromarray(img_array)
            overlay_img.save(output_buffer, format="PNG")
            logger.info("Overlay görüntüsü oluşturuldu")
        
        # Buffer'ı başa sar
        output_buffer.seek(0)
        
        # Doğrudan PNG resmi olarak döndür
        return StreamingResponse(output_buffer, media_type="image/png")

    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error in segmentation process: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        await file.close()

# Segment endpoint (verdiğiniz koda uygun)
@router.post("/segment")
async def segment_image(file: UploadFile = File(...)):
    try:
        logger.info(f"Segment endpoint request received for file: {file.filename}")
        
        # Sadece görüntü dosyası kabul et
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Lütfen bir resim dosyası yükleyin.")
        
        data = await file.read()
        try:
            img = Image.open(io.BytesIO(data))
        except:
            raise HTTPException(status_code=400, detail="Geçersiz resim dosyası.")

        # Ön-işlem
        inp = preprocess_image(img)

        # Model yüklü değilse yükle
        global segmentation_model
        if segmentation_model is None:
            success = load_segmentation_model()
            if not success:
                raise RuntimeError("Segmentasyon modeli yüklenemedi")

        # Tahmin
        pred = segmentation_model.predict(inp)

        # Post-işlem
        mask = postprocess_mask(pred)

        # PNG olarak dön
        buf = io.BytesIO()
        Image.fromarray(mask).save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error in segment process: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        if not file.file.closed:
            await file.close()

# Eski API endpoint'i (JSON döndüren)
@router.post("/segment-image-json", response_model=SegmentationResponse)
async def segment_uploaded_image_json(file: UploadFile = File(...)):
    try:
        logger.info(f"JSON segmentation request received for file: {file.filename}")
        
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
        
        # Dosyayı yeniden aç
        img = Image.open(file_path)
        
        try:
            # Gerçek segmentasyonu gerçekleştir
            mask = perform_segmentation(img)
            
            # Maske görüntüsünü oluştur
            mask_img = Image.fromarray(mask)
            
            # Overlay için orijinal resim üzerine maske uygula
            img_array = np.array(img)
            # Kırmızı kanalı maskele
            img_array[:,:,0] = np.where(mask > 0, 255, img_array[:,:,0])
            # Mavi ve yeşil kanalları hafifçe koyulaştır
            img_array[:,:,1] = np.where(mask > 0, img_array[:,:,1] * 0.7, img_array[:,:,1])
            img_array[:,:,2] = np.where(mask > 0, img_array[:,:,2] * 0.7, img_array[:,:,2])
            
            # Overlay görüntüsünü oluştur
            overlay_img = Image.fromarray(img_array)
        except Exception as seg_err:
            logger.error(f"Error during segmentation: {str(seg_err)}")
            # Hata durumunda boş bir maske ve orjinal resmi dön
            mask_img = Image.new('L', img.size, 0)  # Siyah maske
            overlay_img = img  # Orjinal resim
        
        # Base64'e çevir
        mask_buffer = io.BytesIO()
        mask_img.save(mask_buffer, format="PNG")
        mask_base64 = base64.b64encode(mask_buffer.getvalue()).decode('utf-8')
        
        overlay_buffer = io.BytesIO()
        overlay_img.save(overlay_buffer, format="PNG")
        overlay_base64 = base64.b64encode(overlay_buffer.getvalue()).decode('utf-8')
        
        logger.info("Segmentation completed successfully")
        
        return SegmentationResponse(
            mask_base64=mask_base64,
            overlay_base64=overlay_base64,
            description="Segmentasyon işlemi tamamlandı. Sonuçlar görüntüleniyor."
        )

    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error in segmentation process: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        await file.close()

# URL döndüren endpoint
@router.post("/segment-image-file", response_model=SegmentationImageResponse)
async def segment_image_file(file: UploadFile = File(...)):
    try:
        logger.info(f"File segmentation request received for: {file.filename}")
        
        if not file:
            logger.error("No file uploaded")
            raise HTTPException(status_code=400, detail="Dosya yüklenemedi")
        
        # Izin verilen uzantıları kontrol et
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png"]:
            logger.error(f"Invalid file type: {file_ext}")
            raise HTTPException(status_code=400, detail="Sadece JPG, JPEG ve PNG dosya formatları kabul edilir")
        
        # Orijinal dosyayı kaydet
        orig_filename = f"{uuid.uuid4()}_original.png"
        orig_file_path = os.path.join(UPLOAD_DIR, orig_filename)
        
        # Maske dosyası için isim oluştur
        mask_filename = f"{uuid.uuid4()}_mask.png"
        mask_file_path = os.path.join(UPLOAD_DIR, mask_filename)
        
        logger.info(f"Saving files to: {orig_file_path} and {mask_file_path}")
        
        # Dosyayı oku
        file_bytes = await file.read()
        
        # Orijinal dosyayı kaydet
        with open(orig_file_path, "wb") as buffer:
            buffer.write(file_bytes)
        
        # Dosyayı yeniden aç
        img = Image.open(orig_file_path)
        
        try:
            # Gerçek segmentasyonu gerçekleştir
            mask = perform_segmentation(img)
            
            # Maske görüntüsünü oluştur ve kaydet
            mask_img = Image.fromarray(mask)
            mask_img.save(mask_file_path, format="PNG")
            
            # Overlay için orijinal resim üzerine maske uygula
            img_array = np.array(img)
            # Kırmızı kanalı maskele
            img_array[:,:,0] = np.where(mask > 0, 255, img_array[:,:,0])
            # Mavi ve yeşil kanalları hafifçe koyulaştır
            img_array[:,:,1] = np.where(mask > 0, img_array[:,:,1] * 0.7, img_array[:,:,1])
            img_array[:,:,2] = np.where(mask > 0, img_array[:,:,2] * 0.7, img_array[:,:,2])
            
            # Overlay görüntüsünü oluştur ve kaydet
            overlay_img = Image.fromarray(img_array)
            overlay_img.save(orig_file_path, format="PNG")
            
            logger.info("Segmentation with file output completed successfully")
        except Exception as seg_err:
            logger.error(f"Error during segmentation: {str(seg_err)}")
            # Hata durumunda boş bir maske oluştur
            mask_img = Image.new('L', img.size, 0)  # Siyah maske
            mask_img.save(mask_file_path, format="PNG")
            # Orjinal resmi değiştirmeden kullan
        
        # Dosya URL'lerini oluştur
        overlay_url = f"{STATIC_URL}/{orig_filename}"
        mask_url = f"{STATIC_URL}/{mask_filename}"
        
        return SegmentationImageResponse(
            mask_url=mask_url,
            overlay_url=overlay_url,
            description="Segmentasyon işlemi tamamlandı. Sonuçlar görüntüleniyor."
        )

    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error in segmentation process: {str(e)}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        # Dosya nesnesini kapat
        await file.close()

# Doğrudan belirli bir görüntüyü almak için endpoint
@router.get("/segment-images/{image_type}/{image_id}")
async def get_segmentation_image(
    image_type: str = Path(..., description="Görüntü tipi (mask veya overlay)"),
    image_id: str = Path(..., description="Görüntü ID'si")
):
    try:
        if image_type not in ["mask", "overlay"]:
            raise HTTPException(status_code=400, detail="Geçersiz görüntü tipi. 'mask' veya 'overlay' olmalıdır.")
        
        # İstenen görüntü için dosya yolunu oluştur
        filename = f"{image_id}.png"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Dosyanın varlığını kontrol et
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Görüntü bulunamadı")
        
        # Görüntüyü doğrudan döndür
        return FileResponse(file_path, media_type="image/png")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Görüntü alınırken hata oluştu: {str(e)}")
