from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.company import PlanType, StatusType


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    corporate_domain: str = Field(..., min_length=1, max_length=255)
    plan: PlanType = PlanType.BASIC
    status: StatusType = StatusType.ACTIVE


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    corporate_domain: Optional[str] = Field(None, min_length=1, max_length=255)
    plan: Optional[PlanType] = None
    status: Optional[StatusType] = None


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
