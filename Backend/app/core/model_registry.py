import tensorflow as tf
import os
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    Uygulamanın kullandığı modellerin merkezi kaydı.
    """
    
    # Modeller
    classifier_model = None
    segmenter_model = None
    
    @classmethod
    def load_models(cls):
        """
        Tüm modelleri yükler
        """
        logger.info("Modeller yükleniyor...")
        cls.load_classifier_model()
        cls.load_segmenter_model()
        logger.info("Tüm modeller yüklendi.")
        
    @classmethod
    def load_classifier_model(cls):
        """
        Sınıflandırma modelini yükler
        """
        try:
            # Model yükleme
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "solar_model.keras")
            
            if os.path.exists(model_path):
                logger.info(f"Sınıflandırma modeli yükleniyor: {model_path}")
                cls.classifier_model = tf.keras.models.load_model(model_path)
                logger.info("Sınıflandırma modeli başarıyla yüklendi")
            else:
                # Alternatif: Servis kodu içindeki modeli kullan
                from app.services.classifier import classifier_model
                if classifier_model is not None:
                    cls.classifier_model = classifier_model
                    logger.info("Sınıflandırma modeli servis kodundan alındı")
                else:
                    logger.warning(f"Sınıflandırma modeli bulunamadı: {model_path}")
        except Exception as e:
            logger.error(f"Sınıflandırma modeli yüklenirken hata: {str(e)}")
            # Modeli yükleyemezsek hata verme, sadece log
    
    @classmethod
    def load_segmenter_model(cls):
        """
        Segmentasyon modelini yükler
        """
        try:
            # Segmentasyon modeli yükleme
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "segmentation_model.keras")
            
            if os.path.exists(model_path):
                logger.info(f"Segmentasyon modeli yükleniyor: {model_path}")
                cls.segmenter_model = tf.keras.models.load_model(model_path)
                logger.info("Segmentasyon modeli başarıyla yüklendi")
            else:
                logger.warning(f"Segmentasyon modeli bulunamadı: {model_path}")
        except Exception as e:
            logger.error(f"Segmentasyon modeli yüklenirken hata: {str(e)}")
            # Modeli yükleyemezsek hata verme, sadece log
