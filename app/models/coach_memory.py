from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.core.db_utils import UUID, generate_uuid


class CoachMemory(Base):
    __tablename__ = "coach_memory"

    id = Column(UUID(), primary_key=True, default=generate_uuid, index=True)
    user_language_profile_id = Column(UUID(), ForeignKey("user_language_profiles.id"), nullable=False, unique=True, index=True)
    memory_md = Column(Text, nullable=False)  # arquivo coach_memory.md completo — injetado no system prompt
    recurring_errors = Column(JSON, nullable=True)  # array de { error, weight: float, last_seen: date }
    confirmed_improvements = Column(JSON, nullable=True)  # array de { skill, confirmed_at: date }
    next_focus = Column(Text, nullable=True)  # próximo foco sugerido pelo coach
    sessions_total = Column(Integer, default=0, nullable=False)  # contador de sessões realizadas
    last_compression_at = Column(DateTime, nullable=True)  # quando o job de compressão rodou pela última vez
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user_language_profile = relationship("UserLanguageProfile", back_populates="coach_memory")
