from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.session_plan import SessionPlan, SessionPlanCreate, SessionPlanUpdate
from app.crud import session_plan as crud_plan

router = APIRouter(prefix="/plans", tags=["session_plans"])


@router.get("/", response_model=List[SessionPlan])
def list_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all session plans"""
    plans = crud_plan.get_plans(db, skip=skip, limit=limit)
    return plans


@router.get("/{plan_id}", response_model=SessionPlan)
def get_plan(plan_id: UUID, db: Session = Depends(get_db)):
    """Get a specific session plan by ID"""
    plan = crud_plan.get_plan(db, plan_id=plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Session plan not found")
    return plan


@router.get("/profile/{profile_id}", response_model=List[SessionPlan])
def get_plans_by_profile(profile_id: UUID, db: Session = Depends(get_db)):
    """Get all session plans for a specific user language profile"""
    plans = crud_plan.get_plans_by_profile(db, profile_id=profile_id)
    return plans


@router.post("/", response_model=SessionPlan, status_code=status.HTTP_201_CREATED)
def create_plan(plan: SessionPlanCreate, db: Session = Depends(get_db)):
    """Create a new session plan"""
    return crud_plan.create_plan(db=db, plan=plan)


@router.put("/{plan_id}", response_model=SessionPlan)
def update_plan(plan_id: UUID, plan: SessionPlanUpdate, db: Session = Depends(get_db)):
    """Update a session plan"""
    db_plan = crud_plan.update_plan(db, plan_id=plan_id, plan=plan)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Session plan not found")
    return db_plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: UUID, db: Session = Depends(get_db)):
    """Delete a session plan"""
    success = crud_plan.delete_plan(db, plan_id=plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session plan not found")
    return None
