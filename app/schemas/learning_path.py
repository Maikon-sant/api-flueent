from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.learning_path import LanguageType, LevelType


class LearningPathBase(BaseModel):
    company_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    language: LanguageType
    level: LevelType
    objective: Optional[str] = None
    is_active: bool = True


class LearningPathCreate(LearningPathBase):
    pass


class LearningPathUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    language: Optional[LanguageType] = None
    level: Optional[LevelType] = None
    objective: Optional[str] = None
    is_active: Optional[bool] = None


class LearningPathResponse(LearningPathBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
