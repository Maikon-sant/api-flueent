from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.core.db_utils import UUID, generate_uuid


class UserLanguageProfile(Base):
    __tablename__ = "user_language_profiles"

    id = Column(UUID(), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False, index=True)
    native_language = Column(String(10), nullable=False)  # ex: pt-BR
    target_language = Column(String(10), nullable=False)  # ex: en-US
    current_level = Column(String(5), nullable=False)  # A1, A2, B1, B2, C1, C2
    goal = Column(Text, nullable=True)  # ex: trabalho, viagem, moradia
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="language_profiles")
    sessions = relationship("Session", back_populates="user_language_profile", cascade="all, delete-orphan")
    session_plans = relationship("SessionPlan", back_populates="user_language_profile", cascade="all, delete-orphan")
    coach_memory = relationship("CoachMemory", back_populates="user_language_profile", uselist=False, cascade="all, delete-orphan")
