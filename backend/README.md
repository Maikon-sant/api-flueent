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
- `DELETE /api/v1/learning-paths/{id}` - Delete learning path
- `POST /api/v1/learning-paths/{lp_id}/departments/{dept_id}` - Assign path to department
- `DELETE /api/v1/learning-paths/{lp_id}/departments/{dept_id}` - Remove path from department
- `GET /api/v1/learning-paths/{id}/departments` - Get departments for learning path

#### Contents
- `POST /api/v1/contents` - Create a new content
- `GET /api/v1/contents` - List all contents
- `GET /api/v1/contents/{id}` - Get content by ID
- `PUT /api/v1/contents/{id}` - Update content
- `DELETE /api/v1/contents/{id}` - Delete content

#### Enrollments
- `POST /api/v1/enrollments` - Create a new enrollment
- `GET /api/v1/enrollments` - List all enrollments
- `GET /api/v1/enrollments/{id}` - Get enrollment by ID
- `PUT /api/v1/enrollments/{id}` - Update enrollment
- `DELETE /api/v1/enrollments/{id}` - Delete enrollment
- `GET /api/v1/enrollments/departments/{id}/enrollments` - Get department enrollments
- `POST /api/v1/enrollments/departments/{id}/auto-enroll-users` - Auto-enroll department users

#### Reports
- `GET /api/v1/reports/departments/{id}/progress` - Department progress report
- `GET /api/v1/reports/departments/{id}/learning-paths` - Department learning paths report
- `GET /api/v1/reports/learning-paths/{id}/users` - Learning path users report
- `GET /api/v1/reports/company-overview` - Company overview report

### Utility Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /stats` - General platform statistics

## 🗄️ Database Schema

### Main Entities

1. **Company** - Companies using the platform
2. **Department** - Departments within each company
3. **User** - Employees assigned to departments
4. **LearningPath** - Language learning courses
5. **LearningPathDepartment** - Association between paths and departments
6. **Content** - Content items within learning paths
7. **Enrollment** - User enrollments in learning paths

### Key Relationships

- Company → Departments (1:N)
- Company → Users (1:N)
- Company → Learning Paths (1:N)
- Department → Users (1:N)
- Learning Path → Contents (1:N)
- Learning Path ↔ Departments (N:M)
- User ↔ Learning Paths (N:M through Enrollments)

## 🔒 Business Rules & Validations

- User email must be unique
- User must belong to a department (required)
- Department must belong to the same company as the user
- Learning path must belong to the same company as the department when linking
- Progress must be between 0 and 100
- Duplicate links between learning path and department are prevented
- Duplicate enrollments for the same user and learning path are prevented

## 📊 Example Usage Flow

1. **Create a company**
```bash
POST /api/v1/companies
{
  "name": "My Company",
  "corporate_domain": "mycompany.com",
  "plan": "enterprise"
}
```

2. **Create departments**
```bash
POST /api/v1/departments
{
  "company_id": 1,
  "name": "Sales",
  "description": "Sales team"
}
```

3. **Create a learning path**
```bash
POST /api/v1/learning-paths
{
  "company_id": 1,
  "title": "Business English",
  "language": "english",
  "level": "intermediate"
}
```

4. **Assign learning path to department**
```bash
POST /api/v1/learning-paths/1/departments/1
```

5. **Create users in the department**
```bash
POST /api/v1/users
{
  "company_id": 1,
  "department_id": 1,
  "full_name": "John Doe",
  "email": "john@mycompany.com",
  "role": "employee"
}
```

6. **Auto-enroll all department users**
```bash
POST /api/v1/enrollments/departments/1/auto-enroll-users
```

## 🧪 Testing

You can test the API using:

1. **Swagger UI**: http://localhost:8000/docs
2. **Postman/Insomnia**: Import the OpenAPI spec from http://localhost:8000/openapi.json
3. **cURL**: Command-line HTTP requests
4. **Python requests**: Write integration tests

## 🔄 Database Migrations (Optional)

If you need to modify the database schema:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   └── dependencies.py    # Dependency injection
│   ├── models/                # SQLAlchemy models
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── user.py
│   │   ├── learning_path.py
│   │   ├── learning_path_department.py
│   │   ├── content.py
│   │   └── enrollment.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── user.py
│   │   ├── learning_path.py
│   │   ├── content.py
│   │   └── enrollment.py
│   ├── crud/                  # CRUD operations
│   │   ├── company.py
│   │   ├── department.py
│   │   ├── user.py
│   │   ├── learning_path.py
│   │   ├── learning_path_department.py
│   │   ├── content.py
│   │   └── enrollment.py
│   ├── api/
│   │   └── v1/               # API version 1 routes
│   │       ├── router.py
│   │       ├── company.py
│   │       ├── department.py
│   │       ├── user.py
│   │       ├── learning_path.py
│   │       ├── content.py
│   │       ├── enrollment.py
│   │       └── report.py
│   └── utils/
│       └── seed.py           # Database seeding script
├── alembic/                  # Database migrations
│   ├── versions/
│   └── env.py
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── run.py                  # Application runner
└── README.md              # This file
```

## 🌟 Key Features Details

### Auto-Enrollment
When you assign a learning path to a department and want to enroll all existing users, use the auto-enrollment endpoint:
```
POST /api/v1/enrollments/departments/{department_id}/auto-enroll-users
```

### Progress Tracking
Each enrollment tracks:
- Progress percentage (0-100)
- Status (not_started, in_progress, completed, cancelled)
- Start and completion dates

### Reports
Comprehensive reporting system:
- Department progress overview
- Learning paths by department
- User enrollments by learning path
- Company-wide overview

## 🔐 Environment Configuration

The `.env` file contains:

```env
DATABASE_URL=sqlite:///./flueent.db
APP_NAME=Flueent API
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

For production, change:
- `DEBUG=False`
- Use PostgreSQL or MySQL instead of SQLite
- Update CORS_ORIGINS to your frontend domain
- Add security configurations

## 📝 License

This project is licensed under the MIT License.

## 👥 Support

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using FastAPI**
