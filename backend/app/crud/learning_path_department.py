from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.models.learning_path_department import LearningPathDepartment
from app.models.learning_path import LearningPath
from app.models.department import Department


def get_learning_path_department(
    db: Session, 
    learning_path_id: int, 
    department_id: int
) -> Optional[LearningPathDepartment]:
    return db.query(LearningPathDepartment).filter(
        LearningPathDepartment.learning_path_id == learning_path_id,
        LearningPathDepartment.department_id == department_id
    ).first()


def get_departments_by_learning_path(
    db: Session, 
    learning_path_id: int
) -> List[Department]:
    return db.query(Department).join(
        LearningPathDepartment,
        Department.id == LearningPathDepartment.department_id
    ).filter(
        LearningPathDepartment.learning_path_id == learning_path_id
    ).all()


def get_learning_paths_by_department(
    db: Session, 
    department_id: int
) -> List[LearningPath]:
    return db.query(LearningPath).join(
        LearningPathDepartment,
        LearningPath.id == LearningPathDepartment.learning_path_id
    ).filter(
        LearningPathDepartment.department_id == department_id
    ).all()


def create_learning_path_department(
    db: Session, 
    learning_path_id: int, 
    department_id: int
) -> Optional[LearningPathDepartment]:
    try:
        db_association = LearningPathDepartment(
            learning_path_id=learning_path_id,
            department_id=department_id
        )
        db.add(db_association)
        db.commit()
        db.refresh(db_association)
        return db_association
    except IntegrityError:
        db.rollback()
        return None


def delete_learning_path_department(
    db: Session, 
    learning_path_id: int, 
    department_id: int
) -> bool:
    db_association = get_learning_path_department(db, learning_path_id, department_id)
    if not db_association:
        return False
    
    db.delete(db_association)
    db.commit()
    return True
