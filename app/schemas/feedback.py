from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class ErrorDetail(BaseModel):
    error_type: str
    description: str
    example: Optional[str] = None


class FeedbackRequest(BaseModel):
    user_language_profile_id: str = Field(..., description="ID do perfil de idioma do usuário")
    session_ids: Optional[List[str]] = Field(None, description="IDs das sessões específicas (opcional, usa as últimas se não fornecido)")
    max_sessions: int = Field(5, ge=1, le=20, description="Número máximo de sessões a considerar")


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    user_language_profile_id: str
    sessions_analyzed: int
    total_errors: int
    feedback: str = Field(..., description="Feedback gerado pela IA em markdown")
    generated_at: datetime
    model_used: str


class FeedbackSummary(BaseModel):
    total_sessions: int
    common_errors: List[ErrorDetail]
    strengths: List[str]
    recommendations: List[str]
