import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import threading
import cv2
import base64
from io import BytesIO
from PIL import Image

_model = None
_model_lock = threading.Lock()

def load_segmenter_model():
    global _model
    with _model_lock:
        if _model is None:
            _model = load_model("app/models/segmenter.h5")
    return _model

def preprocess_image(img_path, target_size=(256, 256)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def postprocess_mask(mask):
    mask = np.argmax(mask[0], axis=-1)
    mask = (mask * 85).astype(np.uint8)  
    return mask

def mask_to_base64(mask):
    pil_img = Image.fromarray(mask)
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def segment_image(img_path):
    model = load_segmenter_model()
    preprocessed = preprocess_image(img_path)
    prediction = model.predict(preprocessed)

    mask = postprocess_mask(prediction)
    mask_base64 = mask_to_base64(mask)

    return {
        "mask_base64": mask_base64
    }
