from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DepartmentBase(BaseModel):
    company_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
