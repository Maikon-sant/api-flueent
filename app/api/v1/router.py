from fastapi import APIRouter
from app.api.v1 import (
    user,
    user_language_profile,
    session,
    session_plan,
    session_plan_item,
    coach_memory,
    feedback
)

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(user_language_profile.router)
api_router.include_router(session.router)
api_router.include_router(session_plan.router)
api_router.include_router(session_plan_item.router)
api_router.include_router(coach_memory.router)
api_router.include_router(feedback.router)

