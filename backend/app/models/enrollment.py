from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class EnrollmentStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False, index=True)
    progress = Column(Float, default=0.0, nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.NOT_STARTED, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="enrollments")
    learning_path = relationship("LearningPath", back_populates="enrollments")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'learning_path_id', name='unique_user_learning_path'),
        CheckConstraint('progress >= 0 AND progress <= 100', name='check_progress_range'),
    )
