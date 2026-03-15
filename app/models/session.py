from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.core.db_utils import UUID, generate_uuid


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(), primary_key=True, default=generate_uuid, index=True)
    user_language_profile_id = Column(UUID(), ForeignKey("user_language_profiles.id"), nullable=False, index=True)
    session_type = Column(String(50), nullable=False)  # diagnostic | pronunciation_drill | vocabulary | free_conversation
    duration_seconds = Column(Integer, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    feedback_raw = Column(Text, nullable=True)  # arquivo session_YYYYMMDD.md gerado pela IA (markdown)
    errors_observed = Column(JSON, nullable=True)  # array de erros detectados na sessão
    improvements_observed = Column(JSON, nullable=True)  # array de melhorias detectadas
    coach_note = Column(Text, nullable=True)  # observação livre gerada pelo coach no fim da sessão

    # Relationships
    user_language_profile = relationship("UserLanguageProfile", back_populates="sessions")
    session_plan = relationship("SessionPlan", back_populates="diagnostic_session", uselist=False)
    completed_plan_items = relationship("SessionPlanItem", foreign_keys="SessionPlanItem.completed_session_id", back_populates="completed_session")
