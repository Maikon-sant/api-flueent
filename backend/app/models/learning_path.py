from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class LanguageType(str, enum.Enum):
    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"
    PORTUGUESE = "portuguese"
    ITALIAN = "italian"
    MANDARIN = "mandarin"


class LevelType(str, enum.Enum):
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    UPPER_INTERMEDIATE = "upper_intermediate"
    ADVANCED = "advanced"
    PROFICIENT = "proficient"


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    language = Column(Enum(LanguageType), nullable=False)
    level = Column(Enum(LevelType), nullable=False)
    objective = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="learning_paths")
    contents = relationship("Content", back_populates="learning_path", cascade="all, delete-orphan")
    department_associations = relationship(
        "LearningPathDepartment", 
        back_populates="learning_path", 
        cascade="all, delete-orphan"
    )
    enrollments = relationship("Enrollment", back_populates="learning_path", cascade="all, delete-orphan")
