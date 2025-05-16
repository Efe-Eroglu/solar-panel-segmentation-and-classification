from pydantic import BaseModel
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    all_probabilities: Dict[str, float]

class SegmentationResponse(BaseModel):
    mask_base64: str
    overlay_base64: str
    description: str

# Dosya URL'leri ile yanıt veren yeni model
class SegmentationImageResponse(BaseModel):
    mask_url: str
    overlay_url: str
    description: str
