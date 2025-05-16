# Backend/app/core/model_registry.py

import os
import logging
import traceback
import tensorflow as tf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    Uygulamanın kullandığı modellerin merkezi kaydı.
    """
    classifier_model = None
    segmenter_model = None

    @classmethod
    def load_models(cls):
        logger.info("Modeller yükleniyor...")
        cls.load_classifier_model()
        cls.load_segmenter_model()
        logger.info("Tüm modeller yüklendi.")

    @classmethod
    def load_classifier_model(cls):
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "model", "solar_model.keras"
            )
            if os.path.exists(model_path):
                logger.info(f"Sınıflandırma modeli yükleniyor (compile=False): {model_path}")
                cls.classifier_model = tf.keras.models.load_model(model_path, compile=False)
                logger.info("Sınıflandırma modeli başarıyla yüklendi")
            else:
                logger.warning(f"Sınıflandırma modeli bulunamadı: {model_path}")
        except Exception as e:
            logger.error(f"Sınıflandırma modeli yüklenirken hata: {e}")

    @classmethod
    def load_segmenter_model(cls):
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "model", "segmentation.h5"
            )
            if os.path.exists(model_path):
                logger.info(f"Segmentasyon modeli yükleniyor (compile=False): {model_path}")
                cls.segmenter_model = tf.keras.models.load_model(model_path, compile=False)
                logger.info("Segmentasyon modeli başarıyla yüklendi")
            else:
                logger.warning(f"Segmentasyon modeli bulunamadı: {model_path}")
        except Exception as e:
            logger.error(f"Segmentasyon modeli yüklenirken hata: {e}")
