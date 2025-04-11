import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import threading

_model = None
_model_lock = threading.Lock()

def load_classifier_model():
    global _model
    with _model_lock:
        if _model is None:
            _model = load_model("app/models/classifier.h5")
    return _model

def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predict_class(img_path):
    model = load_classifier_model()
    preprocessed = preprocess_image(img_path)
    predictions = model.predict(preprocessed)
    
    class_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    
    class_labels = ["normal", "faulty", "snow-covered", "bird-drop","electrical-damage","dusty"]
    
    return {
        "class": class_labels[class_index],
        "confidence": confidence
    }
