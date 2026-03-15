import sqlite3

conn = sqlite3.connect('flueent.db')
cursor = conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('📋 Tabelas no banco (flueent.db):')
for t in tables:
    print(f'  - {t[0]}')
    
print('\n📊 Estrutura da tabela users:')
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()
for col in columns:
    print(f'  - {col[1]} ({col[2]})')

conn.close()
