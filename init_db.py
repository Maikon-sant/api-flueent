"""
Script para inicializar o banco de dados
Cria todas as tabelas baseadas nos modelos SQLAlchemy
"""
from app.core.database import engine, Base
# Importar as classes dos modelos (necessário para registrar no Base.metadata)
from app.models.user import User
from app.models.user_language_profile import UserLanguageProfile
from app.models.session import Session
from app.models.session_plan import SessionPlan
from app.models.session_plan_item import SessionPlanItem
from app.models.coach_memory import CoachMemory


def init_db():
    """Cria todas as tabelas no banco de dados"""
    print("🔄 Iniciando criação das tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")
    print("\nTabelas criadas:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")


if __name__ == "__main__":
    init_db()
