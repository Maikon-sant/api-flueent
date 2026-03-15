from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.user_language_profile import UserLanguageProfile, UserLanguageProfileCreate, UserLanguageProfileUpdate
from app.crud import user_language_profile as crud_profile

router = APIRouter(prefix="/profiles", tags=["user_language_profiles"])


@router.get("/", response_model=List[UserLanguageProfile])
def list_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all user language profiles"""
    profiles = crud_profile.get_profiles(db, skip=skip, limit=limit)
    return profiles


@router.get("/{profile_id}", response_model=UserLanguageProfile)
def get_profile(profile_id: UUID, db: Session = Depends(get_db)):
    """Get a specific user language profile by ID"""
    profile = crud_profile.get_profile(db, profile_id=profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/user/{user_id}", response_model=List[UserLanguageProfile])
def get_profiles_by_user(user_id: UUID, db: Session = Depends(get_db)):
    """Get all language profiles for a specific user"""
    profiles = crud_profile.get_profiles_by_user(db, user_id=user_id)
    return profiles


@router.post("/", response_model=UserLanguageProfile, status_code=status.HTTP_201_CREATED)
def create_profile(profile: UserLanguageProfileCreate, db: Session = Depends(get_db)):
    """Create a new user language profile"""
    return crud_profile.create_profile(db=db, profile=profile)


@router.put("/{profile_id}", response_model=UserLanguageProfile)
def update_profile(profile_id: UUID, profile: UserLanguageProfileUpdate, db: Session = Depends(get_db)):
    """Update a user language profile"""
    db_profile = crud_profile.update_profile(db, profile_id=profile_id, profile=profile)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: UUID, db: Session = Depends(get_db)):
    """Delete a user language profile"""
    success = crud_profile.delete_profile(db, profile_id=profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return None
