from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class LearningPathDepartment(Base):
    __tablename__ = "learning_path_departments"

    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    learning_path = relationship("LearningPath", back_populates="department_associations")
    department = relationship("Department", back_populates="learning_path_associations")

    # Unique constraint to prevent duplicates
    __table_args__ = (
        UniqueConstraint('learning_path_id', 'department_id', name='unique_learning_path_department'),
    )
