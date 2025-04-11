from tensorflow.keras.models import load_model

class ModelRegistry:
    classifier_model = None
    segmenter_model = None

    @classmethod
    def load_models(cls):
        print("🔄 Modeller yükleniyor...")
        cls.classifier_model = load_model("app/models/classifier.h5")
        cls.segmenter_model = load_model("app/models/segmenter.h5")
        print("✅ Modeller başarıyla yüklendi.")
