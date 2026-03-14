from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.learning_path import LearningPath
from app.schemas.learning_path import LearningPathCreate, LearningPathUpdate


def get_learning_path(db: Session, learning_path_id: int) -> Optional[LearningPath]:
    return db.query(LearningPath).filter(LearningPath.id == learning_path_id).first()


def get_learning_paths(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    company_id: Optional[int] = None
) -> List[LearningPath]:
    query = db.query(LearningPath)
    if company_id:
        query = query.filter(LearningPath.company_id == company_id)
    return query.offset(skip).limit(limit).all()


def create_learning_path(db: Session, learning_path: LearningPathCreate) -> LearningPath:
    db_learning_path = LearningPath(**learning_path.model_dump())
    db.add(db_learning_path)
    db.commit()
    db.refresh(db_learning_path)
    return db_learning_path


def update_learning_path(db: Session, learning_path_id: int, learning_path: LearningPathUpdate) -> Optional[LearningPath]:
    db_learning_path = get_learning_path(db, learning_path_id)
    if not db_learning_path:
        return None
    
    update_data = learning_path.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_learning_path, key, value)
    
    db.commit()
    db.refresh(db_learning_path)
    return db_learning_path


def delete_learning_path(db: Session, learning_path_id: int) -> bool:
    db_learning_path = get_learning_path(db, learning_path_id)
    if not db_learning_path:
        return False
    
    db.delete(db_learning_path)
    db.commit()
    return True
