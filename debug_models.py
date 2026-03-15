"""Debug script to check model registration"""
import sys
print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\n--- Importing config ---")
from app.core.config import settings
print(f"DATABASE_URL: {settings.DATABASE_URL}")

print("\n--- Importing database ---")
from app.core.database import engine, Base

print(f"Engine: {engine}")
print(f"Engine URL: {engine.url}")

print("\n--- Importing models ---")
from app.models.user import User
from app.models.user_language_profile import UserLanguageProfile
from app.models.session import Session
from app.models.session_plan import SessionPlan
from app.models.session_plan_item import SessionPlanItem
from app.models.coach_memory import CoachMemory

print("\n--- Models imported ---")
print(f"User: {User}")
print(f"Base: {Base}")
print(f"Base.metadata: {Base.metadata}")

print("\n--- Tables in metadata ---")
for table_name, table in Base.metadata.tables.items():
    print(f"  {table_name}: {table}")
    print(f"    Columns: {[c.name for c in table.columns]}")

print("\n--- Creating tables ---")
Base.metadata.create_all(bind=engine)
print("✅ Done!")

print("\n--- Checking database ---")
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables in DB: {[t[0] for t in tables]}")

for t in tables:
    print(f"\n  Table: {t[0]}")
    cursor.execute(f'PRAGMA table_info({t[0]})')
    columns = cursor.fetchall()
    for col in columns:
        print(f"    - {col[1]} ({col[2]})")

conn.close()
