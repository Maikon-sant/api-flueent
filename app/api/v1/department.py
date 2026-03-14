from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.learning_path import LearningPathResponse
from app.crud import department as crud_department
from app.crud import company as crud_company
from app.crud import learning_path_department as crud_lpd

router = APIRouter()


@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new department",
    description="Create a new department within a company."
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new department with all the information:
    
    - **company_id**: ID of the company
    - **name**: Department name
    - **description**: Department description (optional)
    """
    # Validate company exists
    company = crud_company.get_company(db, department.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return crud_department.create_department(db=db, department=department)


@router.get(
    "/",
    response_model=List[DepartmentResponse],
    summary="List all departments",
    description="Retrieve a list of all departments with optional filtering by company."
)
def list_departments(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = Query(None, description="Filter by company ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all departments with pagination and optional filters.
    """
    departments = crud_department.get_departments(
        db, skip=skip, limit=limit, company_id=company_id
    )
    return departments


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="Get department by ID",
    description="Retrieve a specific department by its ID."
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific department by ID.
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return db_department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="Update department",
    description="Update an existing department's information."
)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a department's information.
    """
    db_department = crud_department.update_department(
        db, department_id=department_id, department=department
    )
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return db_department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete department",
    description="Delete a department by its ID."
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a department.
    """
    success = crud_department.delete_department(db, department_id=department_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return None


@router.get(
    "/{department_id}/learning-paths",
    response_model=List[LearningPathResponse],
    summary="Get learning paths for department",
    description="Retrieve all learning paths assigned to a specific department."
)
def get_department_learning_paths(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all learning paths assigned to a department.
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    learning_paths = crud_lpd.get_learning_paths_by_department(db, department_id=department_id)
    return learning_paths
