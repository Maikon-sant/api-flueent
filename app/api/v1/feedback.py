from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.dependencies import get_db
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.crud import session as crud_session
from app.crud import user_language_profile as crud_profile
from app.utils.ai_service import ollama_service

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/generate", response_model=FeedbackResponse)
async def generate_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Gera feedback personalizado usando IA baseado nas sessões do usuário
    
    - **user_language_profile_id**: ID do perfil de idioma
    - **session_ids**: (Opcional) IDs específicos de sessões para analisar
    - **max_sessions**: Número máximo de sessões a considerar (padrão: 5)
    """
    
    # Verificar se o perfil existe
    profile = crud_profile.get_user_language_profile(db, request.user_language_profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil de idioma não encontrado: {request.user_language_profile_id}"
        )
    
    # Buscar sessões
    if request.session_ids:
        # Sessões específicas
        sessions = [
            crud_session.get_session(db, session_id) 
            for session_id in request.session_ids
        ]
        sessions = [s for s in sessions if s is not None]
    else:
        # Últimas sessões do perfil
        all_sessions = crud_profile.get_sessions(db, request.user_language_profile_id)
        # Ordenar por data (mais recentes primeiro) e limitar
        sessions = sorted(
            all_sessions, 
            key=lambda x: x.started_at, 
            reverse=True
        )[:request.max_sessions]
    
    if not sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma sessão encontrada para gerar feedback"
        )
    
    # Agregar erros e melhorias de todas as sessões
    all_errors = []
    all_improvements = []
    
    for session in sessions:
        if session.errors_observed:
            if isinstance(session.errors_observed, list):
                all_errors.extend(session.errors_observed)
            elif isinstance(session.errors_observed, dict):
                all_errors.append(session.errors_observed)
        
        if session.improvements_observed:
            if isinstance(session.improvements_observed, list):
                all_improvements.extend(session.improvements_observed)
            elif isinstance(session.improvements_observed, dict):
                all_improvements.append(session.improvements_observed)
    
    # Preparar contexto do usuário
    user_context = {
        "native_language": profile.native_language,
        "target_language": profile.target_language,
        "current_level": profile.current_level,
        "goal": profile.goal
    }
    
    # Gerar feedback usando Ollama
    try:
        feedback_text = await ollama_service.generate_feedback(
            errors_list=all_errors,
            improvements_list=all_improvements,
            user_context=user_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao gerar feedback: {str(e)}"
        )
    
    return FeedbackResponse(
        user_language_profile_id=request.user_language_profile_id,
        sessions_analyzed=len(sessions),
        total_errors=len(all_errors),
        feedback=feedback_text,
        generated_at=datetime.utcnow(),
        model_used=ollama_service.model
    )


@router.get("/health")
async def check_ai_service():
    """
    Verifica se o serviço de IA (Ollama) está disponível
    """
    is_available = await ollama_service.check_connection()
    
    if is_available:
        return {
            "status": "healthy",
            "service": "ollama",
            "url": ollama_service.base_url,
            "model": ollama_service.model
        }
    else:
        return {
            "status": "unavailable",
            "service": "ollama",
            "url": ollama_service.base_url,
            "message": "Ollama não está rodando. Execute: ollama serve"
        }
