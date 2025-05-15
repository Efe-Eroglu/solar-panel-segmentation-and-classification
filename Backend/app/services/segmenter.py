import numpy as np
from tensorflow.keras.preprocessing import image
from app.core.model_registry import ModelRegistry
from PIL import Image
import base64
from io import BytesIO
import logging
import traceback
import os
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def preprocess_image(img_path, target_size=(256, 256)):
    try:
        logger.info(f"Preprocessing image for segmentation: {img_path}")
        
        # Dosyanın var olup olmadığını kontrol et
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {img_path}")
            
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        
        # Orijinal görüntüyü kaydet
        logger.info(f"Original image shape: {img_array.shape}, dtype: {img_array.dtype}, min: {np.min(img_array)}, max: {np.max(img_array)}")
        
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        logger.info(f"Preprocessed image shape: {img_array.shape}, dtype: {img_array.dtype}, min: {np.min(img_array)}, max: {np.max(img_array)}")
        logger.info(f"Image preprocessed successfully for segmentation: {img_path}")
        return img_array
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error preprocessing image for segmentation: {str(e)}\n{error_detail}")
        raise

def postprocess_mask(mask, debug_folder="app/static/debug"):
    try:
        logger.info("Postprocessing segmentation mask")
        logger.info(f"Raw prediction shape: {mask.shape}, dtype: {mask.dtype}, min: {np.min(mask)}, max: {np.max(mask)}")
        
        # Segmentasyon modelinizin çıktı şekline göre bu kısmı ayarlayın
        # Eğer model son katmanında softmax kullanıyorsa, argmax kullanmak doğrudur
        # Ancak sadece bir maske çıktısı varsa doğrudan kullanmak gerekir
        
        # Tahmin çıktısının boyutlarını kontrol et
        if len(mask.shape) == 4:
            if mask.shape[3] > 1:  # Çoklu sınıf (softmax çıktısı)
                logger.info("Multi-class segmentation detected, using argmax")
                mask = np.argmax(mask[0], axis=-1)
                # Sınıf sayısına göre renklendirme
                mask = (mask * 85).astype(np.uint8)  # Görselleştirme için ölçeklendirme
            else:  # Tek sınıf (sigmoid çıktısı)
                logger.info("Single class segmentation detected")
                mask = (mask[0, :, :, 0] > 0.5).astype(np.uint8) * 255
        else:
            # Beklenmeyen şekil
            logger.warning(f"Unexpected mask shape: {mask.shape}")
            # Düzeltmeye çalış
            if len(mask.shape) == 3 and mask.shape[0] == 1:
                mask = mask[0]
            mask = (mask > 0.5).astype(np.uint8) * 255
        
        logger.info(f"Processed mask shape: {mask.shape}, dtype: {mask.dtype}, unique values: {np.unique(mask)}")
        
        # Debug: Maske görselini kaydet
        os.makedirs(debug_folder, exist_ok=True)
        debug_path = os.path.join(debug_folder, f"mask_debug_{np.random.randint(1000)}.png")
        Image.fromarray(mask).save(debug_path)
        logger.info(f"Debug mask saved to {debug_path}")
        
        logger.info("Mask postprocessed successfully")
        return mask
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error postprocessing mask: {str(e)}\n{error_detail}")
        raise

def mask_to_base64(mask):
    try:
        logger.info("Converting mask to base64")
        logger.info(f"Mask for base64 conversion - shape: {mask.shape}, dtype: {mask.dtype}, unique values: {np.unique(mask)}")
        
        # Maske için renk atama (görselleştirmeyi iyileştirmek için)
        # Eğer binary maske ise farklı bir renk kullanabiliriz
        if np.max(mask) == 1:
            # Binary maske
            colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
            colored_mask[mask == 1] = [0, 255, 0]  # Yeşil
        elif np.max(mask) <= 255:
            # Tek kanallı (grayscale) maske - mavi tonlarına dönüştür
            colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
            if len(np.unique(mask)) <= 2:  # Binary mask ama 0-255 aralığında
                colored_mask[mask > 0] = [0, 0, 255]  # Mavi
            else:
                # Çok sınıflı maske
                # Her değere farklı bir renk atayalım
                for i, val in enumerate(np.unique(mask)):
                    if val == 0:  # Arkaplan genelde 0'dır
                        continue
                    # HSV renk uzayında eşit aralıklarla renk atama
                    hue = (i * 30) % 180  # HSV'de H: 0-180 arası
                    color = plt.cm.get_cmap('tab10')(i % 10)[:3]  
                    color_rgb = [int(c * 255) for c in color]
                    colored_mask[mask == val] = color_rgb
        else:
            # Beklenmeyen değer aralığı
            logger.warning(f"Unexpected mask value range: {np.min(mask)}-{np.max(mask)}")
            # Normalize et
            mask = (mask / np.max(mask) * 255).astype(np.uint8)
            colored_mask = np.stack([mask, mask, mask], axis=-1)
        
        # Maske görselini oluştur ve base64'e dönüştür
        pil_img = Image.fromarray(colored_mask if 'colored_mask' in locals() else mask)
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        base64_str = base64.b64encode(buffered.getvalue()).decode()
        
        logger.info("Mask converted to base64 successfully")
        return base64_str
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error converting mask to base64: {str(e)}\n{error_detail}")
        raise

def create_overlay_image(original_image_path, mask, opacity=0.5):
    """
    Orijinal görüntü ile segmentasyon maskesini birleştirip overlay oluşturur
    
    Args:
        original_image_path: Orijinal görüntü dosya yolu
        mask: Segmentasyon maskesi (numpy array)
        opacity: Maskenin opaklığı (0-1 arası)
    
    Returns:
        overlay_base64: Base64 kodlanmış overlay görüntüsü
    """
    try:
        logger.info(f"Creating overlay image with mask and original image: {original_image_path}")
        
        # Orijinal görüntüyü yükle
        orig_img = Image.open(original_image_path)
        orig_img = orig_img.resize((256, 256))  # Maskeyle aynı boyuta getir
        orig_array = np.array(orig_img)
        
        # Renkli maske oluştur
        if np.max(mask) == 1:
            # Binary maske
            colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
            colored_mask[mask == 1] = [0, 255, 0]  # Yeşil
        elif np.max(mask) <= 255:
            # Grayscale maske
            colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
            if len(np.unique(mask)) <= 2:  # Binary mask ama 0-255 aralığında
                colored_mask[mask > 0] = [255, 0, 0]  # Kırmızı (hasarlı bölgeler için)
            else:
                # Çok sınıflı maske
                for i, val in enumerate(np.unique(mask)):
                    if val == 0:  # Arkaplan
                        continue
                    color = plt.cm.get_cmap('jet')(i % 10)[:3]
                    color_rgb = [int(c * 255) for c in color]
                    colored_mask[mask == val] = color_rgb
        else:
            # Normalize et
            mask = (mask / np.max(mask) * 255).astype(np.uint8)
            colored_mask = np.stack([mask, mask, mask], axis=-1)
        
        # Maske kanalını ekleyelim (alpha kanalı gibi)
        mask_binary = (mask > 0).astype(np.uint8)
        
        # Overlay görüntüsünü oluştur
        overlay = orig_array.copy()
        for c in range(3):  # RGB kanalları
            overlay[:,:,c] = orig_array[:,:,c] * (1 - opacity * mask_binary) + colored_mask[:,:,c] * opacity * mask_binary
        
        # Görüntüyü base64'e dönüştür
        overlay_img = Image.fromarray(overlay.astype(np.uint8))
        buffered = BytesIO()
        overlay_img.save(buffered, format="PNG")
        overlay_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        logger.info("Overlay image created successfully")
        return overlay_base64
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error creating overlay image: {str(e)}\n{error_detail}")
        raise

def segment_image(img_path):
    try:
        logger.info(f"Starting segmentation for image: {img_path}")
        
        # Model kontrolü
        if ModelRegistry.segmenter_model is None:
            logger.error("Segmentation model is not loaded")
            raise ValueError("Segmentasyon modeli yüklenemedi!")
        
        # Modelin yapısını ve katmanlarını log'a yazdır
        logger.info(f"Segmentation model summary: {ModelRegistry.segmenter_model.summary()}")
        
        preprocessed = preprocess_image(img_path)
        logger.info("Image preprocessed, running segmentation")
        
        prediction = ModelRegistry.segmenter_model.predict(preprocessed)
        logger.info(f"Segmentation prediction completed. Output shape: {prediction.shape}")
        
        # Orijinal görüntüyü de kaydet (karşılaştırma için)
        orig_img = Image.open(img_path)
        debug_path = os.path.join("app/static/debug", f"original_{os.path.basename(img_path)}")
        orig_img.save(debug_path)
        logger.info(f"Original image saved to {debug_path}")
        
        mask = postprocess_mask(prediction)
        mask_base64 = mask_to_base64(mask)
        
        # Overlay görüntüsünü oluştur
        overlay_base64 = create_overlay_image(img_path, mask, opacity=0.6)
        
        result = {
            "mask_base64": mask_base64,
            "overlay_base64": overlay_base64
        }
        logger.info("Segmentation process completed successfully")
        
        return result
        
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"Error during segmentation: {str(e)}\n{error_detail}")
        raise
