from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.content import ContentType, ThemeType, SkillType


class ContentBase(BaseModel):
    learning_path_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content_type: ContentType
    theme: ThemeType
    skill: SkillType
    duration_minutes: Optional[int] = Field(None, ge=0)
    order_index: int = Field(0, ge=0)
    is_mandatory: bool = False


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content_type: Optional[ContentType] = None
    theme: Optional[ThemeType] = None
    skill: Optional[SkillType] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    order_index: Optional[int] = Field(None, ge=0)
    is_mandatory: Optional[bool] = None


class ContentResponse(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
