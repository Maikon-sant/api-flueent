from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.coach_memory import CoachMemory, CoachMemoryCreate, CoachMemoryUpdate
from app.crud import coach_memory as crud_memory

router = APIRouter(prefix="/coach-memory", tags=["coach_memory"])


@router.get("/", response_model=List[CoachMemory])
def list_memories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all coach memories"""
    memories = crud_memory.get_memories(db, skip=skip, limit=limit)
    return memories


@router.get("/{memory_id}", response_model=CoachMemory)
def get_memory(memory_id: UUID, db: Session = Depends(get_db)):
    """Get a specific coach memory by ID"""
    memory = crud_memory.get_memory(db, memory_id=memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Coach memory not found")
    return memory


@router.get("/profile/{profile_id}", response_model=CoachMemory)
def get_memory_by_profile(profile_id: UUID, db: Session = Depends(get_db)):
    """Get coach memory for a specific user language profile"""
    memory = crud_memory.get_memory_by_profile(db, profile_id=profile_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Coach memory not found for this profile")
    return memory


@router.post("/", response_model=CoachMemory, status_code=status.HTTP_201_CREATED)
def create_memory(memory: CoachMemoryCreate, db: Session = Depends(get_db)):
    """Create a new coach memory"""
    # Check if memory already exists for this profile
    existing = crud_memory.get_memory_by_profile(db, profile_id=memory.user_language_profile_id)
    if existing:
        raise HTTPException(status_code=400, detail="Coach memory already exists for this profile")
    return crud_memory.create_memory(db=db, memory=memory)


@router.put("/{memory_id}", response_model=CoachMemory)
def update_memory(memory_id: UUID, memory: CoachMemoryUpdate, db: Session = Depends(get_db)):
    """Update a coach memory"""
    db_memory = crud_memory.update_memory(db, memory_id=memory_id, memory=memory)
    if not db_memory:
        raise HTTPException(status_code=404, detail="Coach memory not found")
    return db_memory


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(memory_id: UUID, db: Session = Depends(get_db)):
    """Delete a coach memory"""
    success = crud_memory.delete_memory(db, memory_id=memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Coach memory not found")
    return None
