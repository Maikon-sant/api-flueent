from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import RoleType, LanguageLevel, UserStatus


class UserBase(BaseModel):
    company_id: int
    department_id: int
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: RoleType = RoleType.EMPLOYEE
    job_title: Optional[str] = Field(None, max_length=255)
    language_level: Optional[LanguageLevel] = None
    target_language: Optional[str] = Field(None, max_length=50)
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    department_id: Optional[int] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[RoleType] = None
    job_title: Optional[str] = Field(None, max_length=255)
    language_level: Optional[LanguageLevel] = None
    target_language: Optional[str] = Field(None, max_length=50)
    status: Optional[UserStatus] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
