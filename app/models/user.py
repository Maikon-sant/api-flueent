from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.core.db_utils import UUID, generate_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(), primary_key=True, default=generate_uuid, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    language_profiles = relationship("UserLanguageProfile", back_populates="user", cascade="all, delete-orphan")
