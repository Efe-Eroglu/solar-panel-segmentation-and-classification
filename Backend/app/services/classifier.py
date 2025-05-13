import numpy as np
from tensorflow.keras.preprocessing import image
from app.core.model_registry import ModelRegistry
import logging
import traceback
import os

logger = logging.getLogger(__name__)

def preprocess_image(img_path, target_size=(224, 224)):
    try:
        logger.info(f"Preprocessing image: {img_path}")
        
        # Dosyanın var olup olmadığını kontrol et
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {img_path}")
            
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        logger.info(f"Image preprocessed successfully: {img_path}")
        return img_array
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error preprocessing image: {str(e)}\n{error_detail}")
        raise

def predict_class(img_path):
    try:
        logger.info(f"Starting classification for image: {img_path}")
        
        # Model kontrolü
        if ModelRegistry.classifier_model is None:
            logger.error("Classification model is not loaded")
            raise ValueError("Sınıflandırma modeli yüklenemedi!")
            
        preprocessed = preprocess_image(img_path)
        logger.info("Image preprocessed, running prediction")
        
        predictions = ModelRegistry.classifier_model.predict(preprocessed)
        
        class_index = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        
        class_labels = ['Bird-Drop', 'Clean', 'Dusty', 'Electrical-Damage', 'Physical-Damage', 'Snow-Covered']
        
        result = {
            "class": class_labels[class_index],
            "confidence": confidence
        }
        
        logger.info(f"Classification completed: {result}")
        return result
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error during classification: {str(e)}\n{error_detail}")
        raise
