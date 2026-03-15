"""
Script de teste para o endpoint de feedback com IA
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"


def test_feedback_health():
    """Testa se o serviço de IA está disponível"""
    print("🩺 Testando saúde do serviço de IA...")
    
    try:
        response = requests.get(f"{API_BASE}/feedback/health")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Serviço: {data.get('service')}")
            print(f"   ✅ Status: {data.get('status')}")
            print(f"   ✅ Modelo: {data.get('model')}")
            
            if data.get('status') == 'unavailable':
                print("\n   ⚠️  Ollama não está rodando!")
                print("   💡 Execute: ollama serve")
                print("   💡 E baixe um modelo: ollama pull llama3.2")
                return False
            return True
        else:
            print(f"   ❌ Erro ao verificar saúde: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False


def create_test_data():
    """Cria dados de teste (usuário, perfil, sessões com erros)"""
    print("\n📝 Criando dados de teste...")
    
    # 1. Criar usuário
    print("   1. Criando usuário...")
    user_data = {
        "name": "Maria Santos",
        "email": f"maria.test.{datetime.now().timestamp()}@example.com"
    }
    response = requests.post(f"{API_BASE}/users/", json=user_data)
    user = response.json()
    print(f"      ✅ Usuário criado: {user['id']}")
    
    # 2. Criar perfil de idioma
    print("   2. Criando perfil de idioma...")
    profile_data = {
        "user_id": user['id'],
        "native_language": "Portuguese",
        "target_language": "English",
        "current_level": "B1",
        "goal": "Improve conversation fluency"
    }
    response = requests.post(f"{API_BASE}/user-language-profiles/", json=profile_data)
    profile = response.json()
    print(f"      ✅ Perfil criado: {profile['id']}")
    
    # 3. Criar sessões com erros
    print("   3. Criando sessões com erros...")
    
    sessions = []
    
    # Sessão 1: Erros de gramática
    session1 = {
        "user_language_profile_id": profile['id'],
        "session_type": "free_conversation",
        "duration_seconds": 900,
        "errors_observed": [
            {
                "type": "verb_tense",
                "description": "Incorrect past tense usage",
                "example": "I go to the store yesterday (should be 'went')"
            },
            {
                "type": "article",
                "description": "Missing article",
                "example": "I need book (should be 'a book')"
            },
            {
                "type": "preposition",
                "description": "Wrong preposition",
                "example": "I'm good in English (should be 'at')"
            }
        ],
        "improvements_observed": [
            {
                "area": "pronunciation",
                "description": "Better pronunciation of 'th' sounds"
            }
        ],
        "coach_note": "Student is making progress but needs to focus on verb tenses"
    }
    response = requests.post(f"{API_BASE}/sessions/", json=session1)
    sessions.append(response.json())
    
    # Sessão 2: Erros de pronúncia
    session2 = {
        "user_language_profile_id": profile['id'],
        "session_type": "pronunciation_drill",
        "duration_seconds": 600,
        "errors_observed": [
            {
                "type": "pronunciation",
                "description": "Difficulty with vowel sounds",
                "example": "Confusion between 'ship' and 'sheep'"
            },
            {
                "type": "pronunciation",
                "description": "Word stress incorrect",
                "example": "PHOtograph vs photoGRAphy"
            }
        ],
        "improvements_observed": [
            {
                "area": "fluency",
                "description": "Speaking more naturally, less hesitation"
            }
        ]
    }
    response = requests.post(f"{API_BASE}/sessions/", json=session2)
    sessions.append(response.json())
    
    # Sessão 3: Mais erros de gramática
    session3 = {
        "user_language_profile_id": profile['id'],
        "session_type": "vocabulary",
        "duration_seconds": 720,
        "errors_observed": [
            {
                "type": "word_choice",
                "description": "Using wrong word",
                "example": "I'm boring (should be 'bored')"
            },
            {
                "type": "verb_tense",
                "description": "Present perfect vs simple past",
                "example": "I lived here for 3 years (should be 'have lived')"
            }
        ],
        "improvements_observed": [
            {
                "area": "vocabulary",
                "description": "Using more advanced vocabulary naturally"
            }
        ]
    }
    response = requests.post(f"{API_BASE}/sessions/", json=session3)
    sessions.append(response.json())
    
    print(f"      ✅ {len(sessions)} sessões criadas")
    
    return {
        "user": user,
        "profile": profile,
        "sessions": sessions
    }


def test_generate_feedback(profile_id):
    """Testa geração de feedback"""
    print("\n🤖 Gerando feedback com IA...")
    print("   ⏳ Isso pode levar alguns segundos...")
    
    feedback_request = {
        "user_language_profile_id": profile_id,
        "max_sessions": 5
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/feedback/generate",
            json=feedback_request,
            timeout=120  # 2 minutos
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n   ✅ Feedback gerado com sucesso!")
            print(f"   📊 Sessões analisadas: {data['sessions_analyzed']}")
            print(f"   🔍 Total de erros: {data['total_errors']}")
            print(f"   🤖 Modelo usado: {data['model_used']}")
            print(f"\n{'='*80}")
            print("FEEDBACK GERADO:")
            print('='*80)
            print(data['feedback'])
            print('='*80)
            return True
        elif response.status_code == 503:
            print(f"   ❌ Serviço indisponível: {response.json()['detail']}")
            return False
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   {response.json()}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao gerar feedback: {e}")
        return False


def main():
    print("🧪 Teste do Endpoint de Feedback com IA\n")
    print("="*80)
    
    # Passo 1: Verificar serviço de IA
    if not test_feedback_health():
        print("\n⚠️  Configure o Ollama antes de continuar!")
        print("    Veja instruções em: OLLAMA_SETUP.md")
        return
    
    # Passo 2: Criar dados de teste
    test_data = create_test_data()
    
    # Passo 3: Gerar feedback
    test_generate_feedback(test_data['profile']['id'])
    
    print("\n✨ Teste concluído!")


if __name__ == "__main__":
    main()
