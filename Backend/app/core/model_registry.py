from tensorflow.keras.models import load_model
import os
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelRegistry:
    classifier_model = None
    segmenter_model = None

    @classmethod
    def load_models(cls):
        try:
            logger.info("🔄 Modeller yükleniyor...")
            
            # Model dosyalarının varlığını kontrol et
            cls_model_path = "app/model/classification_model.keras"
            seg_model_path = "app/model/segmentation_model.h5"
            
            if not os.path.exists(cls_model_path):
                logger.error(f"Classification model file not found at {cls_model_path}")
                raise FileNotFoundError(f"Sınıflandırma model dosyası bulunamadı: {cls_model_path}")
                
            if not os.path.exists(seg_model_path):
                logger.error(f"Segmentation model file not found at {seg_model_path}")
                raise FileNotFoundError(f"Segmentasyon model dosyası bulunamadı: {seg_model_path}")
            
            # Modelleri yükle
            logger.info(f"Loading classification model from {cls_model_path}")
            cls.classifier_model = load_model(cls_model_path)
            logger.info("Classification model loaded successfully")
            
            logger.info(f"Loading segmentation model from {seg_model_path}")
            cls.segmenter_model = load_model(seg_model_path)
            logger.info("Segmentation model loaded successfully")
            
            logger.info("✅ Modeller başarıyla yüklendi.")
            
        except Exception as e:
            error_detail = traceback.format_exc()
            logger.error(f"❌ Model yükleme hatası: {str(e)}\n{error_detail}")
            raise Exception(f"Model yükleme sırasında hata oluştu: {str(e)}")
