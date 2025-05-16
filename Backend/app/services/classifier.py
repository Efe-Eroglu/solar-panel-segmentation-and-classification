import numpy as np
import tensorflow as tf
from PIL import Image
import io
import logging
import traceback
import os

logger = logging.getLogger(__name__)

# Model ve sınıf isimleri
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "solar_model.keras")
try:
    classifier_model = tf.keras.models.load_model(model_path)
    logger.info(f"Sınıflandırma modeli başarıyla yüklendi: {model_path}")
except Exception as e:
    logger.error(f"Sınıflandırma modeli yüklenirken hata oluştu: {e}")
    classifier_model = None

# Modelin kullandığı sınıf adları
class_names = [
    'Bird-drop', 
    'Clean', 
    'Dusty', 
    'Electrical-damage', 
    'Physical-damage', 
    'Snow-covered'
]

# Frontend'de kullanılan sınıf adları
frontend_classes = ["normal", "bird-drop", "dusty", "electrical-damage", "faulty", "snow-covered"]
backend_classes = ["clean", "bird-drop", "dusty", "electrical-damage", "physical-damage", "snow-covered"]

def preprocess_image(img_path=None, img_bytes=None, target_size=(244, 244)):
    """
    Görüntüyü sınıflandırma için hazırlar.
    img_path ve img_bytes'dan biri sağlanmalıdır.
    """
    try:
        logger.info(f"Görüntü ön işlemesi başlatılıyor")
        
        if img_path:
            # Dosyadan yükleme
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Dosya bulunamadı: {img_path}")
            
            img = Image.open(img_path).convert('RGB')
            logger.info(f"Görüntü dosyadan yüklendi: {img_path}")
            
        elif img_bytes:
            # Byte dizisinden yükleme
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            logger.info("Görüntü byte dizisinden yüklendi")
            
        else:
            raise ValueError("Görüntü yüklenemedi: img_path veya img_bytes sağlanmalı")
        
        # Boyutlandırma
        img = img.resize(target_size)
        img_array = np.array(img)
        
        # VGG16 preprocessing
        img_array = tf.keras.applications.vgg16.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        logger.info(f"Ön işleme tamamlandı: {img_array.shape}, min: {np.min(img_array)}, max: {np.max(img_array)}")
        return img_array
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Ön işleme hatası: {str(e)}\n{error_detail}")
        raise

def predict_class(img_path=None, img_bytes=None):
    """
    Görüntüyü sınıflandırır.
    img_path veya img_bytes'dan biri sağlanmalıdır.
    """
    try:
        logger.info("Sınıflandırma başlatıldı")
        
        # Model kontrolü
        if classifier_model is None:
            error_msg = "Sınıflandırma modeli yüklenemedi"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        # Ön işleme
        if img_path:
            logger.info(f"Dosyadan sınıflandırma: {img_path}")
            preprocessed = preprocess_image(img_path=img_path)
        elif img_bytes:
            logger.info("Byte dizisinden sınıflandırma")
            preprocessed = preprocess_image(img_bytes=img_bytes)
        else:
            raise ValueError("Görüntü yüklenemedi: img_path veya img_bytes sağlanmalı")
        
        logger.info("Tahmin yapılıyor...")
        
        # Tahmin
        predictions = classifier_model.predict(preprocessed)
        
        # Softmax ile olasılık dağılımına çevir
        probs = tf.nn.softmax(predictions[0]).numpy()
        
        # Sonuçları logla
        logger.info(f"Ham tahmin değerleri: {predictions[0]}")
        logger.info(f"Softmax sonrası olasılıklar: {probs}")
        
        # En yüksek olasılıklı sınıf
        class_index = int(np.argmax(probs))
        confidence = float(probs[class_index])
        backend_class = backend_classes[class_index]
        
        # Backend sınıf adını frontende olan karşılığını bul
        for i, bc in enumerate(backend_classes):
            if bc == backend_class:
                frontend_class = frontend_classes[i]
                break
        else:
            frontend_class = "unknown"
        
        # Her sınıfın olasılıklarını hesapla
        all_probabilities = {}
        for i, backend_class in enumerate(backend_classes):
            frontend_class = frontend_classes[i]
            all_probabilities[frontend_class] = float(probs[i])
        
        logger.info(f"Tahmin sınıfı: {frontend_class}, güven: {confidence:.4f}")
        
        result = {
            "class": frontend_class,
            "confidence": confidence,
            "all_probabilities": all_probabilities
        }
        
        logger.info("Sınıflandırma tamamlandı")
        return result
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Sınıflandırma hatası: {str(e)}\n{error_detail}")
        raise 