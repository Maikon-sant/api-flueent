from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from app.core.config import settings
from app.core.database import engine, get_db, SessionLocal
from app.models import company, department, user, learning_path, learning_path_department, content, enrollment
from app.api.v1.router import api_router

# Create all tables
company.Base.metadata.create_all(bind=engine)
department.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
learning_path.Base.metadata.create_all(bind=engine)
learning_path_department.Base.metadata.create_all(bind=engine)
content.Base.metadata.create_all(bind=engine)
enrollment.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Corporate Language Learning Platform API - A SaaS B2B solution for managing language learning paths by company departments",
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
        "message": "Welcome to Flueent API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json"
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
