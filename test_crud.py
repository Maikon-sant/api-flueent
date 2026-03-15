"""
Teste direto do modelo User
"""
from app.core.database import SessionLocal
from app.crud import user as crud_user
from app.schemas.user import UserCreate
import traceback

db = SessionLocal()

try:
    print("🧪 Testando operações CRUD diretamente...")
    
    # 1. Listar usuários (deve estar vazio)
    print("\n1. Listando usuários...")
    users = crud_user.get_users(db)
    print(f"   ✅ Encontrado: {len(users)} usuários")
    
    # 2. Criar um usuário de teste
    print("\n2. Criando usuário de teste...")
    user_data = UserCreate(
        name="João Silva",
        email="joao@example.com"
    )
    new_user = crud_user.create_user(db, user_data)
    print(f"   ✅ Usuário criado:")
    print(f"      ID: {new_user.id}")
    print(f"      Nome: {new_user.name}")
    print(f"     Email: {new_user.email}")
    
    # 3. Buscar usuário criado
    print("\n3. Buscando usuário criado...")
    found_user = crud_user.get_user(db, new_user.id)
    print(f"   ✅ Usuário encontrado: {found_user.name}")
    
    # 4. Listar novamente
    print("\n4. Listando usuários novamente...")
    users = crud_user.get_users(db)
    print(f"   ✅ Total: {len(users)} usuário(s)")
    for u in users:
        print(f"      - {u.name} ({u.email})")
    
    print("\n✨ Todos os testes passaram!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    print("\nTraceback completo:")
    traceback.print_exc()
finally:
    db.close()
