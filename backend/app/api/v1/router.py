from fastapi import APIRouter
from app.api.v1 import company, department, user, learning_path, content, enrollment, report

api_router = APIRouter()

api_router.include_router(company.router, prefix="/companies", tags=["Companies"])
api_router.include_router(department.router, prefix="/departments", tags=["Departments"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(learning_path.router, prefix="/learning-paths", tags=["Learning Paths"])
api_router.include_router(content.router, prefix="/contents", tags=["Contents"])
api_router.include_router(enrollment.router, prefix="/enrollments", tags=["Enrollments"])
api_router.include_router(report.router, prefix="/reports", tags=["Reports"])
