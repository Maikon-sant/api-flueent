from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.learning_path import LearningPathCreate, LearningPathUpdate, LearningPathResponse
from app.schemas.department import DepartmentResponse
from app.crud import learning_path as crud_learning_path
from app.crud import company as crud_company
from app.crud import department as crud_department
from app.crud import learning_path_department as crud_lpd

router = APIRouter()


@router.post(
    "/",
    response_model=LearningPathResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new learning path",
    description="Create a new learning path within a company."
)
def create_learning_path(
    learning_path: LearningPathCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new learning path with all the information:
    
    - **company_id**: ID of the company
    - **title**: Learning path title
    - **description**: Learning path description (optional)
    - **language**: Target language
    - **level**: Difficulty level
    - **objective**: Learning objective (optional)
    - **is_active**: Whether the path is active
    """
    # Validate company exists
    company = crud_company.get_company(db, learning_path.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return crud_learning_path.create_learning_path(db=db, learning_path=learning_path)


@router.get(
    "/",
    response_model=List[LearningPathResponse],
    summary="List all learning paths",
    description="Retrieve a list of all learning paths with optional filtering."
)
def list_learning_paths(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = Query(None, description="Filter by company ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all learning paths with pagination and optional filters.
    """
    learning_paths = crud_learning_path.get_learning_paths(
        db, skip=skip, limit=limit, company_id=company_id
    )
    return learning_paths


@router.get(
    "/{learning_path_id}",
    response_model=LearningPathResponse,
    summary="Get learning path by ID",
    description="Retrieve a specific learning path by its ID."
)
def get_learning_path(
    learning_path_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific learning path by ID.
    """
    db_learning_path = crud_learning_path.get_learning_path(db, learning_path_id=learning_path_id)
    if db_learning_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    return db_learning_path


@router.put(
    "/{learning_path_id}",
    response_model=LearningPathResponse,
    summary="Update learning path",
    description="Update an existing learning path's information."
)
def update_learning_path(
    learning_path_id: int,
    learning_path: LearningPathUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a learning path's information.
    """
    db_learning_path = crud_learning_path.update_learning_path(
        db, learning_path_id=learning_path_id, learning_path=learning_path
    )
    if db_learning_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    return db_learning_path


@router.delete(
    "/{learning_path_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete learning path",
    description="Delete a learning path by its ID."
)
def delete_learning_path(
    learning_path_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a learning path.
    """
    success = crud_learning_path.delete_learning_path(db, learning_path_id=learning_path_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    return None


@router.post(
    "/{learning_path_id}/departments/{department_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Assign learning path to department",
    description="Create an association between a learning path and a department."
)
def assign_learning_path_to_department(
    learning_path_id: int,
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Assign a learning path to a department.
    """
    # Validate learning path exists
    learning_path = crud_learning_path.get_learning_path(db, learning_path_id)
    if not learning_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    # Validate department exists
    department = crud_department.get_department(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # Validate they belong to the same company
    if learning_path.company_id != department.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Learning path and department must belong to the same company"
        )
    
    # Create association
    association = crud_lpd.create_learning_path_department(
        db, learning_path_id=learning_path_id, department_id=department_id
    )
    
    if not association:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This learning path is already assigned to this department"
        )
    
    return {"message": "Learning path successfully assigned to department"}


@router.delete(
    "/{learning_path_id}/departments/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove learning path from department",
    description="Remove the association between a learning path and a department."
)
def remove_learning_path_from_department(
    learning_path_id: int,
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove a learning path from a department.
    """
    success = crud_lpd.delete_learning_path_department(
        db, learning_path_id=learning_path_id, department_id=department_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association not found"
        )
    
    return None


@router.get(
    "/{learning_path_id}/departments",
    response_model=List[DepartmentResponse],
    summary="Get departments for learning path",
    description="Retrieve all departments assigned to a specific learning path."
)
def get_learning_path_departments(
    learning_path_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all departments assigned to a learning path.
    """
    learning_path = crud_learning_path.get_learning_path(db, learning_path_id=learning_path_id)
    if learning_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    departments = crud_lpd.get_departments_by_learning_path(db, learning_path_id=learning_path_id)
    return departments
