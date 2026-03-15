"""
Teste rápido da API
"""
import requests
import json

try:
    print("🧪 Testando API...")
    
    # Testar endpoint raiz
    print("\n1. Testando endpoint raiz...")
    response = requests.get("http://localhost:8000/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Resposta: {response.json()}")
    
    # Testar health
    print("\n2. Testando /health...")
    response = requests.get("http://localhost:8000/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Resposta: {response.json()}")
    
    # Testar listagem de usuários
    print("\n3. Testando /api/v1/users/...")
    response = requests.get("http://localhost:8000/api/v1/users/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Resposta: {response.json()}")
    else:
        print(f"   ❌ Erro: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Erro: Servidor não está rodando!")
    print("   Execute: python run.py")
except Exception as e:
    print(f"\n❌ Erro: {e}")
