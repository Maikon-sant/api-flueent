from pydantic import BaseModel
from datetime import datetime


class LearningPathDepartmentCreate(BaseModel):
    learning_path_id: int
    department_id: int


class LearningPathDepartmentResponse(BaseModel):
    id: int
    learning_path_id: int
    department_id: int
    assigned_at: datetime

    class Config:
        from_attributes = True
