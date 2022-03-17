from datetime import datetime
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, Relationship

# , JSON
from typing import Optional
from sqlalchemy.dialects.postgresql import JSON


class InferenceBase(SQLModel):
    text: str = Field(nullable=False, index=True)
    candidate_labels: list[str] = Field(
        nullable=False, index=True, sa_column=Column(JSON)
    )
    # result: dict[str, float]


class Inference(InferenceBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    result: dict[str, str] = Field(sa_column=Column(JSON))
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(
        # back_populates="inference"
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Inference.created_by_id == User.id",
        }
    )
