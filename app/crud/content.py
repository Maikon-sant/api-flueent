from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate


def get_content(db: Session, content_id: int) -> Optional[Content]:
    return db.query(Content).filter(Content.id == content_id).first()


def get_contents(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    learning_path_id: Optional[int] = None
) -> List[Content]:
    query = db.query(Content)
    if learning_path_id:
        query = query.filter(Content.learning_path_id == learning_path_id)
    return query.order_by(Content.order_index).offset(skip).limit(limit).all()


def create_content(db: Session, content: ContentCreate) -> Content:
    db_content = Content(**content.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content


def update_content(db: Session, content_id: int, content: ContentUpdate) -> Optional[Content]:
    db_content = get_content(db, content_id)
    if not db_content:
        return None
    
    update_data = content.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_content, key, value)
    
    db.commit()
    db.refresh(db_content)
    return db_content


def delete_content(db: Session, content_id: int) -> bool:
    db_content = get_content(db, content_id)
    if not db_content:
        return False
    
    db.delete(db_content)
    db.commit()
    return True
