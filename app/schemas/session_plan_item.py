from pydantic import BaseModel
from uuid import UUID


class SessionPlanItemBase(BaseModel):
    plan_id: UUID
    order_index: int
    title: str
    focus: str
    session_type: str
    duration_minutes: int
    unlocked: bool = False


class SessionPlanItemCreate(SessionPlanItemBase):
    pass


class SessionPlanItemUpdate(BaseModel):
    unlocked: bool | None = None
    completed_session_id: UUID | None = None


class SessionPlanItem(SessionPlanItemBase):
    id: UUID
    completed_session_id: UUID | None

    class Config:
        from_attributes = True
