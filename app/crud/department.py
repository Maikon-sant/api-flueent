from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


def get_department(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100, company_id: Optional[int] = None) -> List[Department]:
    query = db.query(Department)
    if company_id:
        query = query.filter(Department.company_id == company_id)
    return query.offset(skip).limit(limit).all()


def create_department(db: Session, department: DepartmentCreate) -> Department:
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(db: Session, department_id: int, department: DepartmentUpdate) -> Optional[Department]:
    db_department = get_department(db, department_id)
    if not db_department:
        return None
    
    update_data = department.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_department, key, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int) -> bool:
    db_department = get_department(db, department_id)
    if not db_department:
        return False
    
    db.delete(db_department)
    db.commit()
    return True
