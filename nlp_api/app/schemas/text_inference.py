from app.models.text_inference import TextInferenceBase
from app.models.user import UserBase
from pydantic import BaseModel
from typing import Optional


class TextInferenceCreate(TextInferenceBase):
    result: dict[str, float]


class TextInferenceRead(TextInferenceBase):
    id: int
    result: dict[str, float]
    created_by: UserBase


class TextInferenceUpdate(BaseModel):
    text: Optional[str] = None
