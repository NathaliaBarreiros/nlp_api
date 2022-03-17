from app.models.inference import InferenceBase
from app.models.user import UserBase
from pydantic import BaseModel
from typing import Optional


# class IInferenceResponse(BaseModel):
#     text: str
#     result: dict[str, float]


class IInferenceCreate(InferenceBase):
    result: dict[str, str]


class IInferenceRead(InferenceBase):
    # id: int
    result: dict[str, str]
    created_by: UserBase


class IInferenceUpdate(BaseModel):
    text: Optional[str] = None
    candidate_labels: Optional[list[str]] = None


class IInferenceReadWithUsers(IInferenceRead):
    created_by: UserBase
