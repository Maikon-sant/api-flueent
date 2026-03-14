from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime
from app.models.enrollment import Enrollment
from app.models.user import User
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate


def get_enrollment(db: Session, enrollment_id: int) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def get_enrollment_by_user_and_path(
    db: Session, 
    user_id: int, 
    learning_path_id: int
) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.learning_path_id == learning_path_id
    ).first()


def get_enrollments(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None,
    learning_path_id: Optional[int] = None
) -> List[Enrollment]:
    query = db.query(Enrollment)
    if user_id:
        query = query.filter(Enrollment.user_id == user_id)
    if learning_path_id:
        query = query.filter(Enrollment.learning_path_id == learning_path_id)
    return query.offset(skip).limit(limit).all()


def get_enrollments_by_department(db: Session, department_id: int) -> List[Enrollment]:
    return db.query(Enrollment).join(
        User,
        Enrollment.user_id == User.id
    ).filter(
        User.department_id == department_id
    ).all()


def create_enrollment(db: Session, enrollment: EnrollmentCreate) -> Optional[Enrollment]:
    try:
        db_enrollment = Enrollment(**enrollment.model_dump())
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment
    except IntegrityError:
        db.rollback()
        return None


def update_enrollment(db: Session, enrollment_id: int, enrollment: EnrollmentUpdate) -> Optional[Enrollment]:
    db_enrollment = get_enrollment(db, enrollment_id)
    if not db_enrollment:
        return None
    
    update_data = enrollment.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_enrollment, key, value)
    
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def delete_enrollment(db: Session, enrollment_id: int) -> bool:
    db_enrollment = get_enrollment(db, enrollment_id)
    if not db_enrollment:
        return False
    
    db.delete(db_enrollment)
    db.commit()
    return True


def auto_enroll_users_in_department(db: Session, department_id: int) -> int:
    """
    Auto-enroll all users in a department to all learning paths assigned to that department.
    Returns the number of enrollments created.
    """
    from app.crud.learning_path_department import get_learning_paths_by_department
    
    # Get all users in the department
    users = db.query(User).filter(User.department_id == department_id).all()
    
    # Get all learning paths assigned to this department
    learning_paths = get_learning_paths_by_department(db, department_id)
    
    enrollments_created = 0
    
    for user in users:
        for learning_path in learning_paths:
            # Check if enrollment already exists
            existing = get_enrollment_by_user_and_path(db, user.id, learning_path.id)
            if not existing:
                enrollment_data = EnrollmentCreate(
                    user_id=user.id,
                    learning_path_id=learning_path.id,
                    progress=0.0,
                    status="not_started"
                )
                created = create_enrollment(db, enrollment_data)
                if created:
                    enrollments_created += 1
    
    return enrollments_created
