from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.enrollment import EnrollmentStatus


class EnrollmentBase(BaseModel):
    user_id: int
    learning_path_id: int
    progress: float = Field(0.0, ge=0, le=100)
    status: EnrollmentStatus = EnrollmentStatus.NOT_STARTED


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    progress: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[EnrollmentStatus] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class EnrollmentResponse(EnrollmentBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
