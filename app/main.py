from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.models import (
    user,
    user_language_profile,
    session,
    session_plan,
    session_plan_item,
    coach_memory
)
from app.api.v1.router import api_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Flueet - AI-powered language learning platform with personalized coaching",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Welcome to Flueet API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "description": "AI-powered language learning platform"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "ok",
        "message": "API is healthy and running"
    }


@app.get("/stats", tags=["Statistics"])
def get_stats():
    """
    Get general statistics about the platform.
    """
    db = SessionLocal()
    try:
        from app.models.company import Company
        from app.models.department import Department
        from app.models.user import User
        from app.models.learning_path import LearningPath
        from app.models.content import Content
        from app.models.enrollment import Enrollment
        
        total_companies = db.query(func.count(Company.id)).scalar()
        total_departments = db.query(func.count(Department.id)).scalar()
        total_users = db.query(func.count(User.id)).scalar()
        total_learning_paths = db.query(func.count(LearningPath.id)).scalar()
        total_contents = db.query(func.count(Content.id)).scalar()
        total_enrollments = db.query(func.count(Enrollment.id)).scalar()
        
        return {
            "total_companies": total_companies,
            "total_departments": total_departments,
            "total_users": total_users,
            "total_learning_paths": total_learning_paths,
            "total_contents": total_contents,
            "total_enrollments": total_enrollments
        }
    finally:
        db.close()
