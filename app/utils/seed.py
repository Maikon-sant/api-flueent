"""
Seed script to populate the database with initial data.
Run this after creating the database to have example data.
"""
from datetime import datetime
from app.core.database import SessionLocal
from app.models.company import Company, PlanType, StatusType
from app.models.department import Department
from app.models.user import User, RoleType, LanguageLevel, UserStatus
from app.models.learning_path import LearningPath, LanguageType, LevelType
from app.models.learning_path_department import LearningPathDepartment
from app.models.content import Content, ContentType, ThemeType, SkillType
from app.models.enrollment import Enrollment, EnrollmentStatus


def seed_database():
    """
    Seed the database with initial example data.
    """
    db = SessionLocal()
    
    try:
        print("Starting database seed...")
        
        # Check if data already exists
        existing_company = db.query(Company).first()
        if existing_company:
            print("Database already contains data. Skipping seed.")
            return
        
        # Create Company
        print("Creating company...")
        company = Company(
            name="TechCorp International",
            corporate_domain="techcorp.com",
            plan=PlanType.ENTERPRISE,
            status=StatusType.ACTIVE
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        print(f"✓ Company created: {company.name}")
        
        # Create Departments
        print("Creating departments...")
        dept_sales = Department(
            company_id=company.id,
            name="Sales",
            description="Sales and Business Development team"
        )
        dept_it = Department(
            company_id=company.id,
            name="IT",
            description="Information Technology department"
        )
        dept_hr = Department(
            company_id=company.id,
            name="Human Resources",
            description="HR and People Operations"
        )
        dept_marketing = Department(
            company_id=company.id,
            name="Marketing",
            description="Marketing and Communications"
        )
        
        db.add_all([dept_sales, dept_it, dept_hr, dept_marketing])
        db.commit()
        db.refresh(dept_sales)
        db.refresh(dept_it)
        db.refresh(dept_hr)
        db.refresh(dept_marketing)
        print(f"✓ Departments created: {dept_sales.name}, {dept_it.name}, {dept_hr.name}, {dept_marketing.name}")
        
        # Create Users
        print("Creating users...")
        users_data = [
            # Sales Department
            {
                "company_id": company.id,
                "department_id": dept_sales.id,
                "full_name": "John Smith",
                "email": "john.smith@techcorp.com",
                "role": RoleType.MANAGER,
                "job_title": "Sales Manager",
                "language_level": LanguageLevel.B1,
                "target_language": "english",
                "status": UserStatus.ACTIVE
            },
            {
                "company_id": company.id,
                "department_id": dept_sales.id,
                "full_name": "Maria Garcia",
                "email": "maria.garcia@techcorp.com",
                "role": RoleType.EMPLOYEE,
                "job_title": "Sales Representative",
                "language_level": LanguageLevel.A2,
                "target_language": "english",
                "status": UserStatus.ACTIVE
            },
            # IT Department
            {
                "company_id": company.id,
                "department_id": dept_it.id,
                "full_name": "David Chen",
                "email": "david.chen@techcorp.com",
                "role": RoleType.MANAGER,
                "job_title": "IT Director",
                "language_level": LanguageLevel.C1,
                "target_language": "english",
                "status": UserStatus.ACTIVE
            },
            {
                "company_id": company.id,
                "department_id": dept_it.id,
                "full_name": "Sarah Johnson",
                "email": "sarah.johnson@techcorp.com",
                "role": RoleType.EMPLOYEE,
                "job_title": "Software Developer",
                "language_level": LanguageLevel.B2,
                "target_language": "english",
                "status": UserStatus.ACTIVE
            },
            # HR Department
            {
                "company_id": company.id,
                "department_id": dept_hr.id,
                "full_name": "Emma Wilson",
                "email": "emma.wilson@techcorp.com",
                "role": RoleType.MANAGER,
                "job_title": "HR Manager",
                "language_level": LanguageLevel.B2,
                "target_language": "english",
                "status": UserStatus.ACTIVE
            },
            # Marketing Department
            {
                "company_id": company.id,
                "department_id": dept_marketing.id,
                "full_name": "Lucas Silva",
                "email": "lucas.silva@techcorp.com",
                "role": RoleType.EMPLOYEE,
                "job_title": "Marketing Analyst",
                "language_level": LanguageLevel.B1,
                "target_language": "english",
                "status": UserStatus.ACTIVE
            }
        ]
        
        users = [User(**user_data) for user_data in users_data]
        db.add_all(users)
        db.commit()
        for user in users:
            db.refresh(user)
        print(f"✓ Users created: {len(users)} users")
        
        # Create Learning Paths
        print("Creating learning paths...")
        lp_business_english = LearningPath(
            company_id=company.id,
            title="Business English Fundamentals",
            description="Essential English for business communications",
            language=LanguageType.ENGLISH,
            level=LevelType.INTERMEDIATE,
            objective="Master basic business English vocabulary and communication skills",
            is_active=True
        )
        
        lp_technical_english = LearningPath(
            company_id=company.id,
            title="Technical English for IT Professionals",
            description="English language course focused on technical terminology",
            language=LanguageType.ENGLISH,
            level=LevelType.UPPER_INTERMEDIATE,
            objective="Develop technical English skills for IT documentation and communication",
            is_active=True
        )
        
        lp_sales_english = LearningPath(
            company_id=company.id,
            title="English for Sales and Negotiation",
            description="Advanced English for sales professionals",
            language=LanguageType.ENGLISH,
            level=LevelType.INTERMEDIATE,
            objective="Enhance sales presentation and negotiation skills in English",
            is_active=True
        )
        
        db.add_all([lp_business_english, lp_technical_english, lp_sales_english])
        db.commit()
        db.refresh(lp_business_english)
        db.refresh(lp_technical_english)
        db.refresh(lp_sales_english)
        print(f"✓ Learning paths created: {lp_business_english.title}, {lp_technical_english.title}, {lp_sales_english.title}")
        
        # Assign Learning Paths to Departments
        print("Assigning learning paths to departments...")
        associations = [
            LearningPathDepartment(learning_path_id=lp_business_english.id, department_id=dept_hr.id),
            LearningPathDepartment(learning_path_id=lp_business_english.id, department_id=dept_marketing.id),
            LearningPathDepartment(learning_path_id=lp_technical_english.id, department_id=dept_it.id),
            LearningPathDepartment(learning_path_id=lp_sales_english.id, department_id=dept_sales.id),
        ]
        db.add_all(associations)
        db.commit()
        print(f"✓ Learning path associations created: {len(associations)} assignments")
        
        # Create Contents for Business English
        print("Creating content items...")
        contents_business = [
            Content(
                learning_path_id=lp_business_english.id,
                title="Introduction to Business English",
                description="Overview of business English fundamentals",
                content_type=ContentType.VIDEO,
                theme=ThemeType.BUSINESS,
                skill=SkillType.LISTENING,
                duration_minutes=15,
                order_index=1,
                is_mandatory=True
            ),
            Content(
                learning_path_id=lp_business_english.id,
                title="Business Email Writing",
                description="Learn to write professional business emails",
                content_type=ContentType.TEXT,
                theme=ThemeType.BUSINESS,
                skill=SkillType.WRITING,
                duration_minutes=30,
                order_index=2,
                is_mandatory=True
            ),
            Content(
                learning_path_id=lp_business_english.id,
                title="Business Vocabulary Quiz",
                description="Test your business vocabulary knowledge",
                content_type=ContentType.QUIZ,
                theme=ThemeType.VOCABULARY,
                skill=SkillType.READING,
                duration_minutes=10,
                order_index=3,
                is_mandatory=False
            )
        ]
        
        # Create Contents for Technical English
        contents_technical = [
            Content(
                learning_path_id=lp_technical_english.id,
                title="Technical Documentation Reading",
                description="Reading and understanding technical documentation",
                content_type=ContentType.TEXT,
                theme=ThemeType.TECHNICAL,
                skill=SkillType.READING,
                duration_minutes=45,
                order_index=1,
                is_mandatory=True
            ),
            Content(
                learning_path_id=lp_technical_english.id,
                title="IT Terminology Exercise",
                description="Practice IT-related vocabulary",
                content_type=ContentType.EXERCISE,
                theme=ThemeType.TECHNICAL,
                skill=SkillType.READING,
                duration_minutes=20,
                order_index=2,
                is_mandatory=True
            )
        ]
        
        # Create Contents for Sales English
        contents_sales = [
            Content(
                learning_path_id=lp_sales_english.id,
                title="Sales Presentation Skills",
                description="Delivering effective sales presentations in English",
                content_type=ContentType.VIDEO,
                theme=ThemeType.BUSINESS,
                skill=SkillType.SPEAKING,
                duration_minutes=25,
                order_index=1,
                is_mandatory=True
            ),
            Content(
                learning_path_id=lp_sales_english.id,
                title="Negotiation Role-Play",
                description="Practice negotiation techniques through interactive scenarios",
                content_type=ContentType.INTERACTIVE,
                theme=ThemeType.CONVERSATION,
                skill=SkillType.SPEAKING,
                duration_minutes=40,
                order_index=2,
                is_mandatory=True
            )
        ]
        
        all_contents = contents_business + contents_technical + contents_sales
        db.add_all(all_contents)
        db.commit()
        print(f"✓ Content items created: {len(all_contents)} items")
        
        # Create Enrollments
        print("Creating enrollments...")
        enrollments = [
            # Sales department enrollments
            Enrollment(
                user_id=users[0].id,  # John Smith
                learning_path_id=lp_sales_english.id,
                progress=45.0,
                status=EnrollmentStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            ),
            Enrollment(
                user_id=users[1].id,  # Maria Garcia
                learning_path_id=lp_sales_english.id,
                progress=20.0,
                status=EnrollmentStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            ),
            # IT department enrollments
            Enrollment(
                user_id=users[2].id,  # David Chen
                learning_path_id=lp_technical_english.id,
                progress=80.0,
                status=EnrollmentStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            ),
            Enrollment(
                user_id=users[3].id,  # Sarah Johnson
                learning_path_id=lp_technical_english.id,
                progress=100.0,
                status=EnrollmentStatus.COMPLETED,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow()
            ),
            # HR department enrollment
            Enrollment(
                user_id=users[4].id,  # Emma Wilson
                learning_path_id=lp_business_english.id,
                progress=60.0,
                status=EnrollmentStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            ),
            # Marketing department enrollment
            Enrollment(
                user_id=users[5].id,  # Lucas Silva
                learning_path_id=lp_business_english.id,
                progress=15.0,
                status=EnrollmentStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            ),
        ]
        
        db.add_all(enrollments)
        db.commit()
        print(f"✓ Enrollments created: {len(enrollments)} enrollments")
        
        print("\n" + "="*50)
        print("✓ Database seeded successfully!")
        print("="*50)
        print(f"\nSummary:")
        print(f"  - Companies: 1")
        print(f"  - Departments: 4")
        print(f"  - Users: {len(users)}")
        print(f"  - Learning Paths: 3")
        print(f"  - Contents: {len(all_contents)}")
        print(f"  - Enrollments: {len(enrollments)}")
        print(f"\nYou can now access the API at http://localhost:8000")
        print(f"API Documentation: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
