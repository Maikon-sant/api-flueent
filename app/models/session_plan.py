from sqlalchemy import Column, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.core.db_utils import UUID, generate_uuid


class SessionPlan(Base):
    __tablename__ = "session_plans"

    id = Column(UUID(), primary_key=True, default=generate_uuid, index=True)
    user_language_profile_id = Column(UUID(), ForeignKey("user_language_profiles.id"), nullable=False, index=True)
    diagnostic_session_id = Column(UUID(), ForeignKey("sessions.id"), nullable=False)
    plan_json = Column(JSON, nullable=False)  # array de sessões com id, title, focus, type, duration_minutes, unlocked
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)  # quando todas as sessões foram concluídas

    # Relationships
    user_language_profile = relationship("UserLanguageProfile", back_populates="session_plans")
    diagnostic_session = relationship("Session", back_populates="session_plan")
    items = relationship("SessionPlanItem", back_populates="plan", cascade="all, delete-orphan")
