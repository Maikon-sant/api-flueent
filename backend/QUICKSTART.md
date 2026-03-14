# Guia Rápido - Flueent API

## 🚀 Início Rápido (Quick Start)

### 1. Preparar ambiente

```bash
cd backend
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Popular banco de dados

```bash
python -m app.utils.seed
```

### 4. Iniciar servidor

```bash
python run.py
```

### 5. Acessar documentação

Abra no navegador: **http://localhost:8000/docs**

---

## 📊 Dados de Exemplo

Após executar o seed, você terá:

### Empresa
- **TechCorp International** (techcorp.com)

### Departamentos
- Sales
- IT
- Human Resources
- Marketing

### Usuários (6 total)
- john.smith@techcorp.com (Sales Manager)
- maria.garcia@techcorp.com (Sales Representative)
- david.chen@techcorp.com (IT Director)
- sarah.johnson@techcorp.com (Software Developer)
- emma.wilson@techcorp.com (HR Manager)
- lucas.silva@techcorp.com (Marketing Analyst)

### Trilhas de Aprendizagem
- Business English Fundamentals
- Technical English for IT Professionals
- English for Sales and Negotiation

---

## 🧪 Testar API

### Exemplo 1: Listar todas as empresas
```bash
GET http://localhost:8000/api/v1/companies
```

### Exemplo 2: Listar departamentos
```bash
GET http://localhost:8000/api/v1/departments
```

### Exemplo 3: Ver trilhas de um departamento
```bash
GET http://localhost:8000/api/v1/departments/1/learning-paths
```

### Exemplo 4: Relatório de progresso do departamento
```bash
GET http://localhost:8000/api/v1/reports/departments/1/progress
```

### Exemplo 5: Matricular automaticamente usuários
```bash
POST http://localhost:8000/api/v1/enrollments/departments/1/auto-enroll-users
```

---

## 📍 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/docs` | Documentação Swagger |
| GET | `/health` | Health check |
| GET | `/stats` | Estatísticas gerais |
| GET | `/api/v1/companies` | Listar empresas |
| GET | `/api/v1/departments` | Listar departamentos |
| GET | `/api/v1/users` | Listar usuários |
| GET | `/api/v1/learning-paths` | Listar trilhas |
| GET | `/api/v1/enrollments` | Listar matrículas |
| GET | `/api/v1/reports/company-overview` | Visão geral |

---

## 🔧 Comandos Úteis

### Recriar banco de dados
```bash
# Deletar flueent.db
# Executar seed novamente
python -m app.utils.seed
```

### Ver logs do servidor
O servidor mostra logs no terminal onde foi iniciado.

### Parar servidor
Pressione `Ctrl + C` no terminal.

---

## 📚 Próximos Passos

1. Explore a documentação em `/docs`
2. Teste os endpoints com exemplos
3. Crie suas próprias empresas e departamentos
4. Configure trilhas de aprendizagem
5. Matricule usuários e acompanhe progresso

---

## ⚡ Dicas

- Use `/docs` para testar endpoints diretamente no navegador
- Todos os CRUDs estão implementados
- A API valida dados automaticamente
- Filtros por `company_id` e `department_id` estão disponíveis
- Progresso deve ser entre 0 e 100
- Emails de usuários devem ser únicos

---

**Pronto para usar! 🎉**
