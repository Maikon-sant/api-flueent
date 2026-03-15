from sqlalchemy.orm import Session
from app.models.session_plan import SessionPlan
from app.schemas.session_plan import SessionPlanCreate, SessionPlanUpdate
from uuid import UUID


def get_plan(db: Session, plan_id: UUID):
    return db.query(SessionPlan).filter(SessionPlan.id == plan_id).first()


def get_plans_by_profile(db: Session, profile_id: UUID):
    return db.query(SessionPlan).filter(SessionPlan.user_language_profile_id == profile_id).all()


def get_plans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SessionPlan).offset(skip).limit(limit).all()


def create_plan(db: Session, plan: SessionPlanCreate):
    db_plan = SessionPlan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_plan(db: Session, plan_id: UUID, plan: SessionPlanUpdate):
    db_plan = get_plan(db, plan_id)
    if not db_plan:
        return None
    
    update_data = plan.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    
    db.commit()
    db.refresh(db_plan)
    return db_plan


def delete_plan(db: Session, plan_id: UUID):
    db_plan = get_plan(db, plan_id)
    if db_plan:
        db.delete(db_plan)
        db.commit()
        return True
    return False
