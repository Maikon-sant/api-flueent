from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.session import Session as SessionSchema, SessionCreate, SessionUpdate
from app.crud import session as crud_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/", response_model=List[SessionSchema])
def list_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all sessions"""
    sessions = crud_session.get_sessions(db, skip=skip, limit=limit)
    return sessions


@router.get("/{session_id}", response_model=SessionSchema)
def get_session(session_id: UUID, db: Session = Depends(get_db)):
    """Get a specific session by ID"""
    session = crud_session.get_session(db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/profile/{profile_id}", response_model=List[SessionSchema])
def get_sessions_by_profile(profile_id: UUID, db: Session = Depends(get_db)):
    """Get all sessions for a specific user language profile"""
    sessions = crud_session.get_sessions_by_profile(db, profile_id=profile_id)
    return sessions


@router.post("/", response_model=SessionSchema, status_code=status.HTTP_201_CREATED)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    """Create a new session"""
    return crud_session.create_session(db=db, session=session)


@router.put("/{session_id}", response_model=SessionSchema)
def update_session(session_id: UUID, session: SessionUpdate, db: Session = Depends(get_db)):
    """Update a session"""
    db_session = crud_session.update_session(db, session_id=session_id, session=session)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: UUID, db: Session = Depends(get_db)):
    """Delete a session"""
    success = crud_session.delete_session(db, session_id=session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return None
