from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.core.database import get_db
from app.crud import department as crud_department
from app.crud import learning_path as crud_learning_path
from app.crud import company as crud_company
from app.crud import enrollment as crud_enrollment
from app.crud import learning_path_department as crud_lpd
from app.models.user import User
from app.models.enrollment import Enrollment
from app.models.learning_path import LearningPath
from app.models.department import Department
from app.models.company import Company

router = APIRouter()


@router.get(
    "/departments/{department_id}/progress",
    summary="Department progress report",
    description="Get progress report for all users in a department."
)
def get_department_progress_report(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed progress report for a department including:
    - Average progress across all enrollments
    - Number of users
    - Number of active enrollments
    - Completion statistics
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # Get all enrollments for users in this department
    enrollments = crud_enrollment.get_enrollments_by_department(db, department_id)
    
    # Get all users in department
    users = db.query(User).filter(User.department_id == department_id).all()
    
    # Calculate statistics
    total_enrollments = len(enrollments)
    active_enrollments = sum(1 for e in enrollments if e.status == "in_progress")
    completed_enrollments = sum(1 for e in enrollments if e.status == "completed")
    avg_progress = sum(e.progress for e in enrollments) / total_enrollments if total_enrollments > 0 else 0
    
    return {
        "department_id": department_id,
        "department_name": db_department.name,
        "total_users": len(users),
        "total_enrollments": total_enrollments,
        "active_enrollments": active_enrollments,
        "completed_enrollments": completed_enrollments,
        "average_progress": round(avg_progress, 2),
        "completion_rate": round((completed_enrollments / total_enrollments * 100), 2) if total_enrollments > 0 else 0
    }


@router.get(
    "/departments/{department_id}/learning-paths",
    summary="Department learning paths report",
    description="Get all learning paths assigned to a department with statistics."
)
def get_department_learning_paths_report(
    department_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all learning paths assigned to a department with enrollment statistics.
    """
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    learning_paths = crud_lpd.get_learning_paths_by_department(db, department_id)
    
    results = []
    for lp in learning_paths:
        # Get enrollments for this learning path from users in this department
        enrollments = db.query(Enrollment).join(User).filter(
            Enrollment.learning_path_id == lp.id,
            User.department_id == department_id
        ).all()
        
        total = len(enrollments)
        completed = sum(1 for e in enrollments if e.status == "completed")
        avg_progress = sum(e.progress for e in enrollments) / total if total > 0 else 0
        
        results.append({
            "learning_path_id": lp.id,
            "title": lp.title,
            "language": lp.language,
            "level": lp.level,
            "total_enrollments": total,
            "completed_enrollments": completed,
            "average_progress": round(avg_progress, 2),
            "completion_rate": round((completed / total * 100), 2) if total > 0 else 0
        })
    
    return {
        "department_id": department_id,
        "department_name": db_department.name,
        "learning_paths": results
    }


@router.get(
    "/learning-paths/{learning_path_id}/users",
    summary="Learning path users report",
    description="Get all users enrolled in a specific learning path with their progress."
)
def get_learning_path_users_report(
    learning_path_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all users enrolled in a learning path with their progress details.
    """
    db_learning_path = crud_learning_path.get_learning_path(db, learning_path_id=learning_path_id)
    if db_learning_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    enrollments = crud_enrollment.get_enrollments(db, learning_path_id=learning_path_id)
    
    users_data = []
    for enrollment in enrollments:
        user = db.query(User).filter(User.id == enrollment.user_id).first()
        department = db.query(Department).filter(Department.id == user.department_id).first()
        
        users_data.append({
            "user_id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "department": department.name,
            "enrollment_status": enrollment.status,
            "progress": enrollment.progress,
            "started_at": enrollment.started_at,
            "completed_at": enrollment.completed_at
        })
    
    # Calculate statistics
    total = len(enrollments)
    completed = sum(1 for e in enrollments if e.status == "completed")
    avg_progress = sum(e.progress for e in enrollments) / total if total > 0 else 0
    
    return {
        "learning_path_id": learning_path_id,
        "title": db_learning_path.title,
        "language": db_learning_path.language,
        "level": db_learning_path.level,
        "total_enrollments": total,
        "completed_enrollments": completed,
        "average_progress": round(avg_progress, 2),
        "users": users_data
    }


@router.get(
    "/company-overview",
    summary="Company overview report",
    description="Get overall statistics and overview for all companies."
)
def get_company_overview_report(
    db: Session = Depends(get_db)
):
    """
    Get comprehensive overview with statistics across all companies.
    """
    companies = crud_company.get_companies(db)
    
    overview = []
    for company in companies:
        departments = db.query(Department).filter(Department.company_id == company.id).all()
        users = db.query(User).filter(User.company_id == company.id).all()
        learning_paths = db.query(LearningPath).filter(LearningPath.company_id == company.id).all()
        
        # Get all enrollments for this company's users
        enrollments = db.query(Enrollment).join(User).filter(
            User.company_id == company.id
        ).all()
        
        total_enrollments = len(enrollments)
        completed = sum(1 for e in enrollments if e.status == "completed")
        avg_progress = sum(e.progress for e in enrollments) / total_enrollments if total_enrollments > 0 else 0
        
        overview.append({
            "company_id": company.id,
            "company_name": company.name,
            "plan": company.plan,
            "status": company.status,
            "total_departments": len(departments),
            "total_users": len(users),
            "total_learning_paths": len(learning_paths),
            "total_enrollments": total_enrollments,
            "completed_enrollments": completed,
            "average_progress": round(avg_progress, 2),
            "completion_rate": round((completed / total_enrollments * 100), 2) if total_enrollments > 0 else 0
        })
    
    return {
        "total_companies": len(companies),
        "companies": overview
    }
