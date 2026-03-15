from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class UserLanguageProfileBase(BaseModel):
    user_id: UUID
    native_language: str
    target_language: str
    current_level: str
    goal: str | None = None


class UserLanguageProfileCreate(UserLanguageProfileBase):
    pass


class UserLanguageProfileUpdate(BaseModel):
    native_language: str | None = None
    target_language: str | None = None
    current_level: str | None = None
    goal: str | None = None


class UserLanguageProfile(UserLanguageProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
