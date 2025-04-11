import numpy as np
from tensorflow.keras.preprocessing import image
from app.core.model_registry import ModelRegistry

def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predict_class(img_path):
    model = ModelRegistry.classifier_model
    preprocessed = preprocess_image(img_path)
    predictions = model.predict(preprocessed)
    
    class_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))
    
    class_labels = ["normal", "faulty", "snow-covered", "bird-drop", "electrical-damage", "dusty"]

    return {
        "class": class_labels[class_index],
        "confidence": confidence
    }
