from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class ContentType(str, enum.Enum):
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    INTERACTIVE = "interactive"


class ThemeType(str, enum.Enum):
    BUSINESS = "business"
    TECHNICAL = "technical"
    GENERAL = "general"
    CONVERSATION = "conversation"
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"


class SkillType(str, enum.Enum):
    LISTENING = "listening"
    SPEAKING = "speaking"
    READING = "reading"
    WRITING = "writing"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content_type = Column(Enum(ContentType), nullable=False)
    theme = Column(Enum(ThemeType), nullable=False)
    skill = Column(Enum(SkillType), nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    order_index = Column(Integer, nullable=False, default=0)
    is_mandatory = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    learning_path = relationship("LearningPath", back_populates="contents")
