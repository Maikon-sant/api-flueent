from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.session_plan_item import SessionPlanItem, SessionPlanItemCreate, SessionPlanItemUpdate
from app.crud import session_plan_item as crud_item

router = APIRouter(prefix="/plan-items", tags=["session_plan_items"])


@router.get("/", response_model=List[SessionPlanItem])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all session plan items"""
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=SessionPlanItem)
def get_item(item_id: UUID, db: Session = Depends(get_db)):
    """Get a specific session plan item by ID"""
    item = crud_item.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Session plan item not found")
    return item


@router.get("/plan/{plan_id}", response_model=List[SessionPlanItem])
def get_items_by_plan(plan_id: UUID, db: Session = Depends(get_db)):
    """Get all items for a specific session plan"""
    items = crud_item.get_items_by_plan(db, plan_id=plan_id)
    return items


@router.post("/", response_model=SessionPlanItem, status_code=status.HTTP_201_CREATED)
def create_item(item: SessionPlanItemCreate, db: Session = Depends(get_db)):
    """Create a new session plan item"""
    return crud_item.create_item(db=db, item=item)


@router.put("/{item_id}", response_model=SessionPlanItem)
def update_item(item_id: UUID, item: SessionPlanItemUpdate, db: Session = Depends(get_db)):
    """Update a session plan item"""
    db_item = crud_item.update_item(db, item_id=item_id, item=item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Session plan item not found")
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: UUID, db: Session = Depends(get_db)):
    """Delete a session plan item"""
    success = crud_item.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session plan item not found")
    return None
