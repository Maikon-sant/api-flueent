# 🚀 Flueet API - AI-Powered Language Learning Platform

Plataforma de aprendizado de idiomas com inteligência artificial construída com FastAPI. Sistema completo com memória de coach personalizada, geração de feedback automático e acompanhamento detalhado de progresso.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)

---

## 🌐 Teste a API Online

**🚀 API em Produção:** 
https://api.simplificagov.com/
https://api.simplificagov.com/docs/
https://api.simplificagov.com:8080

Você pode testar a API sem instalar nada localmente! Acesse:

- **📚 Documentação Interativa (Swagger):** https://api.simplificagov.com/docs
- **📖 Documentação Alternativa (ReDoc):** https://api.simplificagov.com/redoc
- **✅ Health Check:** https://api.simplificagov.com/health
- **🤖 Status da IA:** https://api.simplificagov.com/api/v1/feedback/health

> 💡 **Dica:** Use os mesmos endpoints documentados abaixo, apenas substitua `http://localhost:8000` por `https://api.simplificagov.com`

---

## ✨ Funcionalidades Principais

### 🤖 **IA Coach Personalizada**
- **Feedback Inteligente**: Geração automática de feedback usando IA local (Ollama)
- **Memória do Coach**: Sistema de memória persistente que aprende com cada sessão
- **Análise de Erros**: Detecção e categorização automática de erros recorrentes
- **Recomendações Personalizadas**: Sugestões de estudo baseadas no histórico do aluno

### 📊 **Gestão de Aprendizado**
- **Perfis Multi-idioma**: Usuários podem ter múltiplos perfis de aprendizado
- **Sessões Variadas**: Diagnóstico, pronúncia, vocabulário, conversação livre
- **Planos de Estudo**: Geração de planos personalizados baseados em diagnóstico
- **Acompanhamento de Progresso**: Registro detalhado de melhorias e dificuldades

### 💾 **Multi-Database**
- **MySQL**:

### 🔌 **API RESTful Completa**
- Documentação automática com Swagger UI e ReDoc
- Validação de dados com Pydantic
- CORS configurável
- Health checks e estatísticas

---

## 🛠️ Stack de Tecnologias

**Backend:**
- **FastAPI 0.109.0** - Framework web moderno e performático
- **SQLAlchemy 2.0.25** - ORM com suporte a múltiplos bancos
- **Pydantic 2.5.3** - Validação de dados e serialização

**IA & Machine Learning:**
- **Ollama** - IA local para geração de feedback (LLaMA 3.2)
- **httpx** - Cliente HTTP assíncrono para comunicação com Ollama

**Banco de Dados:**
- **SQLite** - Banco padrão para desenvolvimento
- **PostgreSQL** - Suporte via psycopg2-binary
- **MySQL** - Suporte via pymysql + cryptography

**Ferramentas:**
- **Alembic** - Migrações de banco de dados
- **Uvicorn** - Servidor ASGI de alta performance
- **python-dotenv** - Gerenciamento de configuração

---

## 📋 Pré-requisitos

- **Python 3.11+**
- **pip** (gerenciador de pacotes)
- **Ollama** (opcional, para feedback com IA)
- **MySQL/PostgreSQL** (opcional, para produção)

---

## 🚀 Instalação Rápida

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd api-flueet
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

**Para desenvolvimento (SQLite - padrão):**
```bash
# Criar tabelas
python init_db.py
```

**Para produção (MySQL):**
```bash
# Ver instruções em MYSQL_SETUP.md
```

**Para produção (PostgreSQL):**
```bash
# Ver instruções em DATABASE_SETUP.md
```

### 5. Configure variáveis de ambiente

Crie um arquivo `.env` (ou use o padrão):

```env
# Banco de Dados (escolha um)
DATABASE_URL=sqlite:///./flueent.db                                      # SQLite
# DATABASE_URL=postgresql://user:password@localhost/flueent_db          # PostgreSQL
# DATABASE_URL=mysql+pymysql://user:password@localhost/flueent_db       # MySQL

# Aplicação
APP_NAME=Flueet API
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 6. Inicie o servidor

```bash
python run.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn app.main:app --reload
```

**✅ API disponível em:** http://localhost:8000  
**📚 Documentação:** http://localhost:8000/docs

---

## 🤖 Setup da IA (Opcional)

Para habilitar feedback inteligente com IA:

### 1. Instale o Ollama

- **Windows**: https://ollama.ai/download/windows
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`
- **macOS**: `brew install ollama`

### 2. Baixe o modelo

```bash
ollama pull llama3.2
```

### 3. Inicie o serviço

```bash
ollama serve
```

### 4. Teste o endpoint

```bash
curl http://localhost:8000/api/v1/feedback/health
```

📖 **Documentação completa**: [OLLAMA_SETUP.md](OLLAMA_SETUP.md)

---

## 📡 Endpoints da API

### 🏠 **Geral**
- `GET /` - Informações da API
- `GET /health` - Health check
- `GET /docs` - Documentação Swagger UI
- `GET /redoc` - Documentação ReDoc

### 👤 **Usuários**
- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}` - Buscar usuário
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Deletar usuário

### 🌍 **Perfis de Idioma**
- `POST /api/v1/user-language-profiles/` - Criar perfil
- `GET /api/v1/user-language-profiles/` - Listar perfis
- `GET /api/v1/user-language-profiles/{id}` - Buscar perfil
- `PUT /api/v1/user-language-profiles/{id}` - Atualizar perfil
- `DELETE /api/v1/user-language-profiles/{id}` - Deletar perfil

### 🎯 **Sessões**
- `POST /api/v1/sessions/` - Criar sessão
- `GET /api/v1/sessions/` - Listar sessões
- `GET /api/v1/sessions/{id}` - Buscar sessão
- `PUT /api/v1/sessions/{id}` - Atualizar sessão
- `DELETE /api/v1/sessions/{id}` - Deletar sessão

### 📅 **Planos de Estudo**
- `POST /api/v1/session-plans/` - Criar plano
- `GET /api/v1/session-plans/` - Listar planos
- `GET /api/v1/session-plans/{id}` - Buscar plano
- `PUT /api/v1/session-plans/{id}` - Atualizar plano
- `DELETE /api/v1/session-plans/{id}` - Deletar plano

### 📋 **Itens do Plano**
- `POST /api/v1/session-plan-items/` - Criar item
- `GET /api/v1/session-plan-items/` - Listar itens
- `GET /api/v1/session-plan-items/{id}` - Buscar item
- `PUT /api/v1/session-plan-items/{id}` - Atualizar item
- `DELETE /api/v1/session-plan-items/{id}` - Deletar item

### 🧠 **Coach Memory**
- `POST /api/v1/coach-memory/` - Criar memória
- `GET /api/v1/coach-memory/` - Listar memórias
- `GET /api/v1/coach-memory/{id}` - Buscar memória
- `PUT /api/v1/coach-memory/{id}` - Atualizar memória
- `DELETE /api/v1/coach-memory/{id}` - Deletar memória

### 🤖 **Feedback com IA**
- `POST /api/v1/feedback/generate` - Gerar feedback personalizado
- `GET /api/v1/feedback/health` - Verificar status da IA

📖 **Documentação completa**: [FEEDBACK_API.md](FEEDBACK_API.md)

---

## 🗄️ Schema do Banco de Dados

### **Estrutura de 6 Tabelas**

```
┌──────────────┐
│    users     │
│ ─────────────│
│ id (UUID)    │◄─┐
│ name         │  │
│ email        │  │
│ created_at   │  │
└──────────────┘  │
                  │
┌─────────────────────────┐
│ user_language_profiles  │
│ ────────────────────────│
│ id (UUID)               │◄─┐
│ user_id (FK)            │──┘
│ native_language         │
│ target_language         │
│ current_level           │
│ goal                    │
└─────────────────────────┘
    ▲                ▲
    │                │
    │                ├─────────────────────┐
    │                │                     │
┌───┴────────┐  ┌────┴─────────┐  ┌───────┴───────┐
│  sessions  │  │session_plans │  │ coach_memory  │
│ ───────────│  │ ─────────────│  │ ──────────────│
│ id         │  │ id           │  │ id            │
│ profile_id │  │ profile_id   │  │ profile_id    │
│ type       │  │ plan_json    │  │ memory_md     │
│ errors     │  │ completed_at │  │ next_focus    │
│ feedback   │  └──────────────┘  └───────────────┘
└────────────┘
             ┌─────────────────────┐
             │ session_plan_items  │
             │ ────────────────────│
             │ id                  │
             │ plan_id (FK)        │
             │ order_index         │
             │ title               │
             │ unlocked            │
             └─────────────────────┘
```

### **Tabelas Principais**

1. **users** - Perfil base do usuário
2. **user_language_profiles** - Perfis de aprendizado (um usuário pode ter vários)
3. **sessions** - Sessões de prática/conversação
4. **session_plans** - Planos de estudo personalizados
5. **session_plan_items** - Itens individuais dos planos
6. **coach_memory** - Memória persistente da IA para cada perfil

### **Relacionamentos**
- User → Language Profiles (1:N)
- Language Profile → Sessions (1:N)
- Language Profile → Session Plans (1:N)
- Language Profile → Coach Memory (1:1)
- Session Plan → Plan Items (1:N)

---

## 🎯 Fluxo de Uso Típico

### **1. Criar Usuário**
```bash
POST /api/v1/users/
{
  "name": "Maria Santos",
  "email": "maria@example.com"
}
```

### **2. Criar Perfil de Idioma**
```bash
POST /api/v1/user-language-profiles/
{
  "user_id": "uuid-do-usuario",
  "native_language": "Portuguese",
  "target_language": "English",
  "current_level": "B1",
  "goal": "Business fluency"
}
```

### **3. Registrar Sessão de Prática**
```bash
POST /api/v1/sessions/
{
  "user_language_profile_id": "uuid-do-perfil",
  "session_type": "free_conversation",
  "duration_seconds": 900,
  "errors_observed": [
    {
      "type": "verb_tense",
      "example": "I go yesterday (should be 'went')"
    }
  ]
}
```

### **4. Gerar Feedback com IA**
```bash
POST /api/v1/feedback/generate
{
  "user_language_profile_id": "uuid-do-perfil",
  "max_sessions": 5
}
```

---

## 🧪 Testes

### **Scripts de Teste Disponíveis**

```bash
# Testar conexão com banco
python test_db.py

# Testar operações CRUD
python test_crud.py

# Testar endpoints da API
python test_api.py

# Testar feedback com IA (requer Ollama)
python test_feedback.py
```

### **Testar via Swagger UI**

Acesse: http://localhost:8000/docs

---

## 📁 Estrutura do Projeto

```
api-flueet/
├── app/
│   ├── __init__.py
│   ├── main.py                      # App FastAPI principal
│   ├── api/
│   │   └── v1/
│   │       ├── user.py              # Endpoints de usuários
│   │       ├── user_language_profile.py
│   │       ├── session.py
│   │       ├── session_plan.py
│   │       ├── session_plan_item.py
│   │       ├── coach_memory.py
│   │       ├── feedback.py          # Endpoints de IA
│   │       └── router.py            # Router principal
│   ├── core/
│   │   ├── config.py                # Configurações
│   │   ├── database.py              # Setup do banco
│   │   ├── db_utils.py              # UUID helper
│   │   └── dependencies.py          # Dependências
│   ├── crud/                        # Operações de banco
│   │   ├── user.py
│   │   ├── session.py
│   │   └── ...
│   ├── models/                      # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── session.py
│   │   └── ...
│   ├── schemas/                     # Schemas Pydantic
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── feedback.py
│   │   └── ...
│   └── utils/
│       └── ai_service.py            # Integração Ollama
├── alembic/                         # Migrações
├── tests/                           # Testes
├── .env                             # Variáveis de ambiente
├── requirements.txt                 # Dependências
├── init_db.py                       # Criar tabelas
├── run.py                           # Iniciar servidor
├── test_api.py                      # Testes da API
├── test_crud.py                     # Testes CRUD
├── test_feedback.py                 # Testes IA
├── DATABASE_SETUP.md                # Setup PostgreSQL
├── MYSQL_SETUP.md                   # Setup MySQL
├── OLLAMA_SETUP.md                  # Setup IA
├── FEEDBACK_API.md                  # Doc Feedback
└── README.md                        # Este arquivo
```

---

## 🔒 Regras de Negócio

- ✅ Email de usuário deve ser único
- ✅ UUID como chave primária em todas as tabelas
- ✅ Erros armazenados em JSON para flexibilidade
- ✅ Coach memory único por perfil de idioma
- ✅ Sessões vinculadas a perfis, não diretamente a usuários
- ✅ Relacionamentos com cascade delete configurados

---

## 📝 Variáveis de Ambiente

```env
# Banco de Dados
DATABASE_URL=sqlite:///./flueent.db

# Aplicação
APP_NAME=Flueet API
APP_VERSION=1.0.0
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 🔄 Migrações (Alembic)

```bash
# Criar migração automática
alembic revision --autogenerate -m "Descrição"

# Aplicar migrações
alembic upgrade head

# Reverter
alembic downgrade -1
```

---

## 📚 Documentação Adicional

- 📖 [DATABASE_SETUP.md](DATABASE_SETUP.md) - Configuração PostgreSQL
- 🐬 [MYSQL_SETUP.md](MYSQL_SETUP.md) - Configuração MySQL
- 🤖 [OLLAMA_SETUP.md](OLLAMA_SETUP.md) - Configuração IA
- 💬 [FEEDBACK_API.md](FEEDBACK_API.md) - API de Feedback

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)  
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**🚀 Pronto para começar?**

- **Teste online:** https://api.simplificagov.com/docs
- **Instale localmente:** Execute `python run.py` e acesse http://localhost:8000/docs
│   │   ├── config.py          # Configurações da aplicação
│   │   ├── database.py        # Conexão com o banco de dados
│   │   └── dependencies.py    # Injeção de dependências
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── user.py
│   │   ├── learning_path.py
│   │   ├── learning_path_department.py
│   │   ├── content.py
│   │   └── enrollment.py
│   ├── schemas/               # Schemas Pydantic
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── user.py
│   │   ├── learning_path.py
│   │   ├── content.py
│   │   └── enrollment.py
│   ├── crud/                  # Operações CRUD
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── user.py
│   │   ├── learning_path.py
│   │   ├── learning_path_department.py
│   │   ├── content.py
│   │   └── enrollment.py
│   ├── api/
│   │   └── v1/               # Rotas da API versão 1
│   │       ├── router.py
│   │       ├── company.py
│   │       ├── department.py
│   │       ├── user.py
│   │       ├── learning_path.py
│   │       ├── content.py
│   │       ├── enrollment.py
│   │       └── report.py
│   └── utils/
│       └── seed.py           # Script de população do banco
├── alembic/                  # Migrações do banco de dados
│   ├── versions/
│   └── env.py
├── alembic.ini              # Configuração do Alembic
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente
├── .env.example            # Modelo de variáveis de ambiente
├── .gitignore              # Regras do Git ignore
├── run.py                  # Inicializador da aplicação
└── README.md              # Este arquivo
```

## 🌟 Detalhes das Funcionalidades

### Matrícula Automática
Para matricular todos os usuários existentes de um departamento em uma trilha, use o endpoint de matrícula automática:
```
POST /api/v1/enrollments/departments/{department_id}/auto-enroll-users
```

### Acompanhamento de Progresso
Cada matrícula registra:
- Percentual de progresso (0–100)
- Status (`not_started`, `in_progress`, `completed`, `cancelled`)
- Datas de início e conclusão

### Relatórios
Sistema de relatórios completo:
- Visão geral do progresso por departamento
- Trilhas por departamento
- Usuários matriculados por trilha
- Visão geral da empresa

## 🔐 Configuração de Ambiente

O arquivo `.env` contém:

```env
DATABASE_URL=sqlite:///./flueent.db
APP_NAME=Flueet API
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

Para produção, altere:
- `DEBUG=False`
- Use PostgreSQL ou MySQL no lugar do SQLite
- Atualize `CORS_ORIGINS` para o domínio do seu frontend
- Adicione configurações de segurança adicionais

## 📝 Licença

Este projeto está licenciado sob a Licença MIT.
