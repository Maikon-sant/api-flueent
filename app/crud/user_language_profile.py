from sqlalchemy.orm import Session
from app.models.user_language_profile import UserLanguageProfile
from app.schemas.user_language_profile import UserLanguageProfileCreate, UserLanguageProfileUpdate
from uuid import UUID


def get_user_language_profile(db: Session, profile_id: UUID):
    """Alias para compatibilidade - busca um perfil por ID"""
    return db.query(UserLanguageProfile).filter(UserLanguageProfile.id == profile_id).first()


def get_profile(db: Session, profile_id: UUID):
    return db.query(UserLanguageProfile).filter(UserLanguageProfile.id == profile_id).first()


def get_sessions(db: Session, profile_id: UUID):
    """Retorna todas as sessões de um perfil de idioma"""
    profile = get_profile(db, profile_id)
    if profile:
        return profile.sessions
    return []


def get_profiles_by_user(db: Session, user_id: UUID):
    return db.query(UserLanguageProfile).filter(UserLanguageProfile.user_id == user_id).all()


def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserLanguageProfile).offset(skip).limit(limit).all()


def create_profile(db: Session, profile: UserLanguageProfileCreate):
    db_profile = UserLanguageProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: UUID, profile: UserLanguageProfileUpdate):
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return None
    
    update_data = profile.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: UUID):
    db_profile = get_profile(db, profile_id)
    if db_profile:
        db.delete(db_profile)
        db.commit()
        return True
    return False
