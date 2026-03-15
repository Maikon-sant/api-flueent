from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionUpdate
from uuid import UUID


def get_session(db: Session, session_id: UUID):
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()


def get_sessions_by_profile(db: Session, profile_id: UUID):
    return db.query(SessionModel).filter(SessionModel.user_language_profile_id == profile_id).all()


def get_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SessionModel).offset(skip).limit(limit).all()


def create_session(db: Session, session: SessionCreate):
    db_session = SessionModel(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def update_session(db: Session, session_id: UUID, session: SessionUpdate):
    db_session = get_session(db, session_id)
    if not db_session:
        return None
    
    update_data = session.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_session, key, value)
    
    db.commit()
    db.refresh(db_session)
    return db_session


def delete_session(db: Session, session_id: UUID):
    db_session = get_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
        return True
    return False
