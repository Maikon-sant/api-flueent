from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any


class SessionBase(BaseModel):
    user_language_profile_id: UUID
    session_type: str
    duration_seconds: int


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    ended_at: datetime | None = None
    feedback_raw: str | None = None
    errors_observed: list[dict[str, Any]] | None = None
    improvements_observed: list[dict[str, Any]] | None = None
    coach_note: str | None = None


class Session(SessionBase):
    id: UUID
    started_at: datetime
    ended_at: datetime | None
    feedback_raw: str | None
    errors_observed: list[dict[str, Any]] | None
    improvements_observed: list[dict[str, Any]] | None
    coach_note: str | None

    class Config:
        from_attributes = True
