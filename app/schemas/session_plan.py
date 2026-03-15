from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any


class SessionPlanBase(BaseModel):
    user_language_profile_id: UUID
    diagnostic_session_id: UUID
    plan_json: list[dict[str, Any]]


class SessionPlanCreate(SessionPlanBase):
    pass


class SessionPlanUpdate(BaseModel):
    plan_json: list[dict[str, Any]] | None = None
    completed_at: datetime | None = None


class SessionPlan(SessionPlanBase):
    id: UUID
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True
