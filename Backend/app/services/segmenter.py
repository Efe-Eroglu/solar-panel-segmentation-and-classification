import numpy as np
from tensorflow.keras.preprocessing import image
from app.core.model_registry import ModelRegistry
from PIL import Image
import base64
from io import BytesIO
import logging
import traceback
import os

logger = logging.getLogger(__name__)

def preprocess_image(img_path, target_size=(256, 256)):
    try:
        logger.info(f"Preprocessing image for segmentation: {img_path}")
        
        # Dosyanın var olup olmadığını kontrol et
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {img_path}")
            
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        logger.info(f"Image preprocessed successfully for segmentation: {img_path}")
        return img_array
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error preprocessing image for segmentation: {str(e)}\n{error_detail}")
        raise

def postprocess_mask(mask):
    try:
        logger.info("Postprocessing segmentation mask")
        mask = np.argmax(mask[0], axis=-1)
        mask = (mask * 85).astype(np.uint8)  # Görselleştirme için ölçeklendirme
        logger.info("Mask postprocessed successfully")
        return mask
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error postprocessing mask: {str(e)}\n{error_detail}")
        raise

def mask_to_base64(mask):
    try:
        logger.info("Converting mask to base64")
        pil_img = Image.fromarray(mask)
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        base64_str = base64.b64encode(buffered.getvalue()).decode()
        logger.info("Mask converted to base64 successfully")
        return base64_str
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error converting mask to base64: {str(e)}\n{error_detail}")
        raise

def segment_image(img_path):
    try:
        logger.info(f"Starting segmentation for image: {img_path}")
        
        # Model kontrolü
        if ModelRegistry.segmenter_model is None:
            logger.error("Segmentation model is not loaded")
            raise ValueError("Segmentasyon modeli yüklenemedi!")
        
        preprocessed = preprocess_image(img_path)
        logger.info("Image preprocessed, running segmentation")
        
        prediction = ModelRegistry.segmenter_model.predict(preprocessed)
        logger.info("Segmentation prediction completed")
        
        mask = postprocess_mask(prediction)
        mask_base64 = mask_to_base64(mask)
        
        result = {"mask_base64": mask_base64}
        logger.info("Segmentation process completed successfully")
        
        return result
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error during segmentation: {str(e)}\n{error_detail}")
        raise
