from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from app.crud import enrollment as crud_enrollment
from app.crud import user as crud_user
from app.crud import learning_path as crud_learning_path
from app.crud import department as crud_department

router = APIRouter()


@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new enrollment",
    description="Create a new enrollment for a user in a learning path."
)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new enrollment with all the information:
    
    - **user_id**: ID of the user
    - **learning_path_id**: ID of the learning path
    - **progress**: Progress percentage (0-100)
    - **status**: Enrollment status (not_started, in_progress, completed, cancelled)
    """
    # Validate user exists
    user = crud_user.get_user(db, enrollment.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate learning path exists
    learning_path = crud_learning_path.get_learning_path(db, enrollment.learning_path_id)
    if not learning_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    # Check if enrollment already exists
    existing = crud_enrollment.get_enrollment_by_user_and_path(
        db, enrollment.user_id, enrollment.learning_path_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already enrolled in this learning path"
        )
    
    new_enrollment = crud_enrollment.create_enrollment(db=db, enrollment=enrollment)
    if not new_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create enrollment"
        )
    
    return new_enrollment


@router.get(
    "/",
    response_model=List[EnrollmentResponse],
    summary="List all enrollments",
    description="Retrieve a list of all enrollments with pagination."
)
def list_enrollments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all enrollments with pagination.
    """
    enrollments = crud_enrollment.get_enrollments(db, skip=skip, limit=limit)
    return enrollments


@router.get(
    "/{enrollment_id}",
    response_model=EnrollmentResponse,
    summary="Get enrollment by ID",
    description="Retrieve a specific enrollment by its ID."
)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific enrollment by ID.
    """
    db_enrollment = crud_enrollment.get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return db_enrollment


@router.put(
    "/{enrollment_id}",
    response_model=EnrollmentResponse,
    summary="Update enrollment",
    description="Update an existing enrollment's information."
)
def update_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an enrollment's information.
    """
    db_enrollment = crud_enrollment.update_enrollment(
        db, enrollment_id=enrollment_id, enrollment=enrollment
    )
    if db_enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return db_enrollment


@router.delete(
    "/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete enrollment",
    description="Delete an enrollment by its ID."
)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an enrollment.
    """
    success = crud_enrollment.delete_enrollment(db, enrollment_id=enrollment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return None


@router.get(
    "/departments/{department_id}/enrollments",
    response_model=List[EnrollmentResponse],
    summary="Get enrollments by department",
    description="Retrieve all enrollments for users in a specific department."
)
def get_department_enrollments(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all enrollments for users in a department.
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    enrollments = crud_enrollment.get_enrollments_by_department(db, department_id=department_id)
    return enrollments


@router.post(
    "/departments/{department_id}/auto-enroll-users",
    summary="Auto-enroll department users",
    description="Automatically enroll all users in a department to all learning paths assigned to that department."
)
def auto_enroll_department_users(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Auto-enroll all users in a department to all assigned learning paths.
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    enrollments_created = crud_enrollment.auto_enroll_users_in_department(
        db, department_id=department_id
    )
    
    return {
        "message": f"Successfully auto-enrolled users",
        "enrollments_created": enrollments_created
    }
