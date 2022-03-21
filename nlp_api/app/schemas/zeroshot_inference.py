from app.models.zeroshot_inference import ZeroShotInferenceBase
from app.models.user import UserBase
from pydantic import BaseModel
from typing import Optional


class ZeroShotInferenceCreate(ZeroShotInferenceBase):
    result: dict[str, float]


class ZeroShotInferenceRead(ZeroShotInferenceBase):
    id: int
    result: dict[str, float]
    created_by: UserBase


class ZeroShotInferenceUpdate(BaseModel):
    text: Optional[str] = None
    candidate_labels: Optional[list[str]] = None
