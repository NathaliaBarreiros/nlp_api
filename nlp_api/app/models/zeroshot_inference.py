from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON


class ZeroShotInferenceBase(SQLModel):
    text: str = Field(nullable=False, index=True)
    candidate_labels: list[str] = Field(
        nullable=False, index=True, sa_column=Column(JSON)
    )


class ZeroShotInference(ZeroShotInferenceBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    result: dict[str, float] = Field(nullable=False, sa_column=Column(JSON))
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "ZeroShotInference.created_by_id == User.id",
        }
    )
