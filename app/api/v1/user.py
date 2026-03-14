from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.enrollment import EnrollmentResponse
from app.crud import user as crud_user
from app.crud import company as crud_company
from app.crud import department as crud_department
from app.crud import enrollment as crud_enrollment

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user within a company and department."
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user with all the information:
    
    - **company_id**: ID of the company
    - **department_id**: ID of the department (required)
    - **full_name**: User's full name
    - **email**: User's email (must be unique)
    - **role**: User role (admin, manager, employee)
    - **job_title**: User's job title (optional)
    - **language_level**: Current language level (optional)
    - **target_language**: Target language for learning (optional)
    - **status**: User status (active, inactive)
    """
    # Validate company exists
    company = crud_company.get_company(db, user.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Validate department exists and belongs to the same company
    department = crud_department.get_department(db, user.department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    if department.company_id != user.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department does not belong to the specified company"
        )
    
    # Validate email is unique
    existing_user = crud_user.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return crud_user.create_user(db=db, user=user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users",
    description="Retrieve a list of all users with optional filtering."
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = Query(None, description="Filter by company ID"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all users with pagination and optional filters.
    """
    users = crud_user.get_users(
        db, skip=skip, limit=limit, company_id=company_id, department_id=department_id
    )
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by its ID."
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user's information."
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a user's information.
    """
    # Get existing user
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate department if being updated
    if user.department_id is not None:
        department = crud_department.get_department(db, user.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        if department.company_id != db_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department does not belong to user's company"
            )
    
    # Validate email uniqueness if being updated
    if user.email is not None and user.email != db_user.email:
        existing_user = crud_user.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    updated_user = crud_user.update_user(db, user_id=user_id, user=user)
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by its ID."
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a user.
    """
    success = crud_user.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None


@router.get(
    "/{user_id}/enrollments",
    response_model=List[EnrollmentResponse],
    summary="Get user enrollments",
    description="Retrieve all enrollments for a specific user."
)
def get_user_enrollments(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all enrollments for a specific user.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    enrollments = crud_enrollment.get_enrollments(db, user_id=user_id)
    return enrollments
