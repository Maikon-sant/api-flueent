from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    last_active_at: datetime | None = None


class User(UserBase):
    id: UUID
    created_at: datetime
    last_active_at: datetime

    class Config:
        from_attributes = True
