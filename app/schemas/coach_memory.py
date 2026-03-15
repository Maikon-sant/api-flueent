from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any


class CoachMemoryBase(BaseModel):
    user_language_profile_id: UUID
    memory_md: str


class CoachMemoryCreate(CoachMemoryBase):
    pass


class CoachMemoryUpdate(BaseModel):
    memory_md: str | None = None
    recurring_errors: list[dict[str, Any]] | None = None
    confirmed_improvements: list[dict[str, Any]] | None = None
    next_focus: str | None = None
    sessions_total: int | None = None
    last_compression_at: datetime | None = None


class CoachMemory(CoachMemoryBase):
    id: UUID
    recurring_errors: list[dict[str, Any]] | None
    confirmed_improvements: list[dict[str, Any]] | None
    next_focus: str | None
    sessions_total: int
    last_compression_at: datetime | None
    updated_at: datetime

    class Config:
        from_attributes = True
