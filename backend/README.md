# Flueent API - Corporate Language Learning Platform

A complete backend API built with FastAPI for a B2B SaaS corporate language learning platform. The system focuses on organizing employees by departments and assigning specific learning paths to each department.

## 🚀 Features

- **Multi-company Management**: Support for multiple companies with different subscription plans
- **Department Organization**: Organize employees by departments/sectors
- **Learning Paths**: Create and manage language learning paths with multiple content items
- **Department-Path Association**: Link learning paths to specific departments
- **User Enrollment**: Enroll users in learning paths with progress tracking
- **Auto-enrollment**: Automatically enroll department users in assigned learning paths
- **Comprehensive Reports**: Track progress by department, learning path, and company
- **RESTful API**: Complete CRUD operations for all entities
- **Auto-generated Documentation**: Swagger UI and OpenAPI specification
- **Database Migrations**: Alembic support for schema versioning

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Alembic** - Database migration tool
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)
- **Uvicorn** - ASGI server
- **python-dotenv** - Environment variable management

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (for version control)

## 🔧 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd api-flueent/backend
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

The `.env` file is already configured with default values. You can modify it if needed:

```env
DATABASE_URL=sqlite:///./flueent.db
APP_NAME=Flueent API
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 5. Seed the database

Populate the database with example data:

```bash
python -m app.utils.seed
```

This will create:
- 1 company (TechCorp International)
- 4 departments (Sales, IT, HR, Marketing)
- 6 users across different departments
- 3 learning paths
- Multiple content items
- Sample enrollments with progress tracking

## 🚀 Running the Application

### Start the development server

```bash
python run.py
```

Or use uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📡 API Endpoints

### Core Entities

#### Companies
- `POST /api/v1/companies` - Create a new company
- `GET /api/v1/companies` - List all companies
- `GET /api/v1/companies/{id}` - Get company by ID
- `PUT /api/v1/companies/{id}` - Update company
- `DELETE /api/v1/companies/{id}` - Delete company

#### Departments
- `POST /api/v1/departments` - Create a new department
- `GET /api/v1/departments` - List all departments
- `GET /api/v1/departments/{id}` - Get department by ID
- `PUT /api/v1/departments/{id}` - Update department
- `DELETE /api/v1/departments/{id}` - Delete department
- `GET /api/v1/departments/{id}/learning-paths` - Get learning paths for department

#### Users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `GET /api/v1/users/{id}/enrollments` - Get user enrollments

#### Learning Paths
- `POST /api/v1/learning-paths` - Create a new learning path
- `GET /api/v1/learning-paths` - List all learning paths
- `GET /api/v1/learning-paths/{id}` - Get learning path by ID
- `PUT /api/v1/learning-paths/{id}` - Update learning path
# Flueent API - Plataforma de Aprendizado de Idiomas Corporativo

API backend completa construída com FastAPI para uma plataforma B2B SaaS de aprendizado de idiomas corporativo. O sistema foca em organizar colaboradores por departamentos e atribuir trilhas de aprendizado específicas a cada departamento.

## 🚀 Funcionalidades

- **Gestão Multi-empresa**: Suporte a múltiplas empresas com diferentes planos de assinatura
- **Organização por Departamentos**: Organize colaboradores por departamentos/setores
- **Trilhas de Aprendizado**: Crie e gerencie trilhas de aprendizado de idiomas com múltiplos conteúdos
- **Associação Departamento-Trilha**: Vincule trilhas de aprendizado a departamentos específicos
- **Matrícula de Usuários**: Matricule usuários em trilhas com acompanhamento de progresso
- **Matrícula Automática**: Matricule automaticamente todos os usuários de um departamento nas trilhas atribuídas
- **Relatórios Completos**: Acompanhe o progresso por departamento, trilha e empresa
- **API RESTful**: Operações CRUD completas para todas as entidades
- **Documentação Automática**: Swagger UI e especificação OpenAPI
- **Migrações de Banco**: Suporte ao Alembic para versionamento de schema

## 🛠️ Stack de Tecnologias

- **Python 3.11+**
- **FastAPI** - Framework web moderno para construção de APIs
- **SQLAlchemy** - ORM e toolkit SQL
- **Pydantic** - Validação de dados usando type annotations do Python
- **Alembic** - Ferramenta de migração de banco de dados
- **SQLite** - Banco de dados padrão (facilmente substituível por PostgreSQL/MySQL)
- **Uvicorn** - Servidor ASGI
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para controle de versão)

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd api-flueent/backend
```

### 2. Crie um ambiente virtual

**Windows:**
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
pip install email-validator
```

### 4. Configure as variáveis de ambiente

O arquivo `.env` já vem configurado com valores padrão. Altere se necessário:

```env
DATABASE_URL=sqlite:///./flueent.db
APP_NAME=Flueent API
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 5. Popular o banco de dados

Popule o banco com dados de exemplo:

```bash
python -m app.utils.seed
```

Isso criará:
- 1 empresa (TechCorp International)
- 4 departamentos (Vendas, TI, RH, Marketing)
- 6 usuários distribuídos entre os departamentos
- 3 trilhas de aprendizado
- Múltiplos itens de conteúdo
- Matrículas de exemplo com acompanhamento de progresso

## 🚀 Executando a Aplicação

### Iniciar o servidor de desenvolvimento

```bash
python run.py
```

Ou usando o uvicorn diretamente:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Com o servidor rodando, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📡 Endpoints da API

### Entidades Principais

#### Empresas
- `POST /api/v1/companies` - Criar nova empresa
- `GET /api/v1/companies` - Listar todas as empresas
- `GET /api/v1/companies/{id}` - Buscar empresa por ID
- `PUT /api/v1/companies/{id}` - Atualizar empresa
- `DELETE /api/v1/companies/{id}` - Excluir empresa

#### Departamentos
- `POST /api/v1/departments` - Criar novo departamento
- `GET /api/v1/departments` - Listar todos os departamentos
- `GET /api/v1/departments/{id}` - Buscar departamento por ID
- `PUT /api/v1/departments/{id}` - Atualizar departamento
- `DELETE /api/v1/departments/{id}` - Excluir departamento
- `GET /api/v1/departments/{id}/learning-paths` - Trilhas de aprendizado do departamento

#### Usuários
- `POST /api/v1/users` - Criar novo usuário
- `GET /api/v1/users` - Listar todos os usuários
- `GET /api/v1/users/{id}` - Buscar usuário por ID
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Excluir usuário
- `GET /api/v1/users/{id}/enrollments` - Matrículas do usuário

#### Trilhas de Aprendizado
- `POST /api/v1/learning-paths` - Criar nova trilha
- `GET /api/v1/learning-paths` - Listar todas as trilhas
- `GET /api/v1/learning-paths/{id}` - Buscar trilha por ID
- `PUT /api/v1/learning-paths/{id}` - Atualizar trilha
- `DELETE /api/v1/learning-paths/{id}` - Excluir trilha
- `POST /api/v1/learning-paths/{lp_id}/departments/{dept_id}` - Vincular trilha a departamento
- `DELETE /api/v1/learning-paths/{lp_id}/departments/{dept_id}` - Desvincular trilha de departamento
- `GET /api/v1/learning-paths/{id}/departments` - Departamentos da trilha

#### Conteúdos
- `POST /api/v1/contents` - Criar novo conteúdo
- `GET /api/v1/contents` - Listar todos os conteúdos
- `GET /api/v1/contents/{id}` - Buscar conteúdo por ID
- `PUT /api/v1/contents/{id}` - Atualizar conteúdo
- `DELETE /api/v1/contents/{id}` - Excluir conteúdo

#### Matrículas
- `POST /api/v1/enrollments` - Criar nova matrícula
- `GET /api/v1/enrollments` - Listar todas as matrículas
- `GET /api/v1/enrollments/{id}` - Buscar matrícula por ID
- `PUT /api/v1/enrollments/{id}` - Atualizar matrícula
- `DELETE /api/v1/enrollments/{id}` - Excluir matrícula
- `GET /api/v1/enrollments/departments/{id}/enrollments` - Matrículas do departamento
- `POST /api/v1/enrollments/departments/{id}/auto-enroll-users` - Matrícula automática do departamento

#### Relatórios
- `GET /api/v1/reports/departments/{id}/progress` - Relatório de progresso do departamento
- `GET /api/v1/reports/departments/{id}/learning-paths` - Trilhas do departamento
- `GET /api/v1/reports/learning-paths/{id}/users` - Usuários por trilha
- `GET /api/v1/reports/company-overview` - Visão geral da empresa

### Endpoints Utilitários

- `GET /` - Endpoint raiz com informações da API
- `GET /health` - Verificação de saúde
- `GET /stats` - Estatísticas gerais da plataforma

## 🗄️ Schema do Banco de Dados

### Entidades Principais

1. **Company** - Empresas que utilizam a plataforma
2. **Department** - Departamentos dentro de cada empresa
3. **User** - Colaboradores vinculados a departamentos
4. **LearningPath** - Cursos de aprendizado de idiomas
5. **LearningPathDepartment** - Associação entre trilhas e departamentos
6. **Content** - Itens de conteúdo dentro das trilhas
7. **Enrollment** - Matrículas de usuários nas trilhas

### Relacionamentos

- Empresa → Departamentos (1:N)
- Empresa → Usuários (1:N)
- Empresa → Trilhas de Aprendizado (1:N)
- Departamento → Usuários (1:N)
- Trilha → Conteúdos (1:N)
- Trilha ↔ Departamentos (N:M)
- Usuário ↔ Trilhas (N:M via Matrículas)

## 🔒 Regras de Negócio e Validações

- E-mail do usuário deve ser único
- Usuário deve pertencer a um departamento (obrigatório)
- Departamento deve pertencer à mesma empresa do usuário
- Trilha deve pertencer à mesma empresa do departamento ao vincular
- Progresso deve estar entre 0 e 100
- Vínculos duplicados entre trilha e departamento são impedidos
- Matrículas duplicadas para o mesmo usuário e trilha são impedidas

## 📊 Fluxo de Uso Típico

1. **Criar uma empresa**
```bash
POST /api/v1/companies
{
  "name": "Minha Empresa",
  "corporate_domain": "minhaempresa.com.br",
  "plan": "enterprise"
}
```

2. **Criar departamentos**
```bash
POST /api/v1/departments
{
  "company_id": 1,
  "name": "Vendas",
  "description": "Equipe de vendas"
}
```

3. **Criar uma trilha de aprendizado**
```bash
POST /api/v1/learning-paths
{
  "company_id": 1,
  "title": "Inglês para Negócios",
  "language": "english",
  "level": "intermediate"
}
```

4. **Vincular trilha ao departamento**
```bash
POST /api/v1/learning-paths/1/departments/1
```

5. **Criar usuários no departamento**
```bash
POST /api/v1/users
{
  "company_id": 1,
  "department_id": 1,
  "full_name": "João Silva",
  "email": "joao@minhaempresa.com.br",
  "role": "employee"
}
```

6. **Matricular automaticamente todos os usuários do departamento**
```bash
POST /api/v1/enrollments/departments/1/auto-enroll-users
```

## 🧪 Testes

Você pode testar a API usando:

1. **Swagger UI**: http://localhost:8000/docs
2. **Postman/Insomnia**: Importe a spec OpenAPI de http://localhost:8000/openapi.json
3. **cURL**: Requisições HTTP via linha de comando
4. **Python requests**: Escreva testes de integração

## 🔄 Migrações de Banco de Dados (Opcional)

Para modificar o schema do banco:

```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição das mudanças"

# Aplicar migrações
alembic upgrade head

# Reverter migrações
alembic downgrade -1
```

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada da aplicação FastAPI
│   ├── core/
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
APP_NAME=Flueent API
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

## 👥 Suporte

Para dúvidas ou suporte, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando FastAPI**
