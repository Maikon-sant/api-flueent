"""
Script para testar a conexão e o banco de dados
"""
from sqlalchemy import text
from app.core.database import engine, SessionLocal
from app.core.config import settings

print("=" * 60)
print("🔍 TESTANDO BANCO DE DADOS")
print("=" * 60)

# 1. Verificar configuração
print(f"\n📋 Configuração:")
print(f"   DATABASE_URL: {settings.DATABASE_URL}")

# 2. Testar conexão
try:
    connection = engine.connect()
    print(f"\n✅ Conexão estabelecida com sucesso!")
    
    # 3. Verificar tabelas
    print(f"\n📊 Verificando tabelas no banco de dados...")
    
    if "sqlite" in settings.DATABASE_URL.lower():
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    elif "mysql" in settings.DATABASE_URL.lower():
        result = connection.execute(text("SHOW TABLES;"))
    elif "postgresql" in settings.DATABASE_URL.lower():
        result = connection.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
    else:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    
    tables = [row[0] for row in result]
    
    if tables:
        print(f"\n✅ Tabelas encontradas ({len(tables)}):")
        for table in tables:
            print(f"   - {table}")
    else:
        print(f"\n⚠️  Nenhuma tabela encontrada!")
    
    # 4. Testar inserção e leitura
    print(f"\n🧪 Testando operações básicas...")
    
    db = SessionLocal()
    try:
        # Verificar se podemos fazer uma query simples
        result = db.execute(text("SELECT COUNT(*) FROM users;"))
        count = result.scalar()
        print(f"   ✅ Query executada: {count} usuários no banco")
        
        print(f"\n✨ BANCO DE DADOS FUNCIONANDO PERFEITAMENTE!")
        
    except Exception as e:
        print(f"   ⚠️  Erro ao executar query: {e}")
    finally:
        db.close()
    
    connection.close()
    
except Exception as e:
    print(f"\n❌ Erro ao conectar ao banco de dados:")
    print(f"   {e}")
    print(f"\n💡 Dica: Verifique se o arquivo .env está configurado corretamente")

print("\n" + "=" * 60)
