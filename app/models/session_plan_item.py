from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.db_utils import UUID, generate_uuid


class SessionPlanItem(Base):
    __tablename__ = "session_plan_items"

    id = Column(UUID(), primary_key=True, default=generate_uuid, index=True)
    plan_id = Column(UUID(), ForeignKey("session_plans.id"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)  # posição no plano (1, 2, 3...)
    title = Column(String(200), nullable=False)  # ex: Abertura sem hesitação
    focus = Column(Text, nullable=False)  # problema específico que a sessão ataca
    session_type = Column(String(50), nullable=False)  # pronunciation_drill | vocabulary | free_conversation
    duration_minutes = Column(Integer, nullable=False)
    unlocked = Column(Boolean, default=False, nullable=False)  # default false, primeiro item = true
    completed_session_id = Column(UUID(), ForeignKey("sessions.id"), nullable=True)  # preenchido quando o item for concluído

    # Relationships
    plan = relationship("SessionPlan", back_populates="items")
    completed_session = relationship("Session", foreign_keys=[completed_session_id], back_populates="completed_plan_items")
