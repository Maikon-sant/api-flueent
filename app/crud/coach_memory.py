from sqlalchemy.orm import Session
from app.models.coach_memory import CoachMemory
from app.schemas.coach_memory import CoachMemoryCreate, CoachMemoryUpdate
from uuid import UUID


def get_memory(db: Session, memory_id: UUID):
    return db.query(CoachMemory).filter(CoachMemory.id == memory_id).first()


def get_memory_by_profile(db: Session, profile_id: UUID):
    return db.query(CoachMemory).filter(CoachMemory.user_language_profile_id == profile_id).first()


def get_memories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CoachMemory).offset(skip).limit(limit).all()


def create_memory(db: Session, memory: CoachMemoryCreate):
    db_memory = CoachMemory(**memory.model_dump())
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory


def update_memory(db: Session, memory_id: UUID, memory: CoachMemoryUpdate):
    db_memory = get_memory(db, memory_id)
    if not db_memory:
        return None
    
    update_data = memory.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_memory, key, value)
    
    db.commit()
    db.refresh(db_memory)
    return db_memory


def delete_memory(db: Session, memory_id: UUID):
    db_memory = get_memory(db, memory_id)
    if db_memory:
        db.delete(db_memory)
        db.commit()
        return True
    return False
