from sqlalchemy.orm import Session
from app.models.session_plan_item import SessionPlanItem
from app.schemas.session_plan_item import SessionPlanItemCreate, SessionPlanItemUpdate
from uuid import UUID


def get_item(db: Session, item_id: UUID):
    return db.query(SessionPlanItem).filter(SessionPlanItem.id == item_id).first()


def get_items_by_plan(db: Session, plan_id: UUID):
    return db.query(SessionPlanItem).filter(SessionPlanItem.plan_id == plan_id).order_by(SessionPlanItem.order_index).all()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SessionPlanItem).offset(skip).limit(limit).all()


def create_item(db: Session, item: SessionPlanItemCreate):
    db_item = SessionPlanItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: UUID, item: SessionPlanItemUpdate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: UUID):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
