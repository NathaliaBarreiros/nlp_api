from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON


class TextInferenceBase(SQLModel):
    text: str = Field(nullable=False, index=True)


class TextInference(TextInferenceBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    result: dict[str, float] = Field(nullable=False, sa_column=Column(JSON))
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "TextInference.created_by_id == User.id",
        }
    )
