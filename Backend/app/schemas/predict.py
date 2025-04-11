from pydantic import BaseModel

class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float

class SegmentationResponse(BaseModel):
    mask_base64: str
    description: str
