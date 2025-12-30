import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import sys
import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database.config import Base, get_db
from app.main import app
from app.database.models import Tenant, Student, Skill, Course, RoleCluster, SkillRelationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_tenant(db):
    tenant = Tenant(name="Test University", country="UK", branding_config={})
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@pytest.fixture
def test_student(db, test_tenant):
    student = Student(
        tenant_id=test_tenant.id,
        name="Test Student",
        email="test@example.com",
        university="Test University",
        graduation_year=2025
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@pytest.fixture
def test_skills(db, test_tenant):
    skills = [
        Skill(tenant_id=test_tenant.id, name="Python Programming", category="Technical", description="Python skills"),
        Skill(tenant_id=test_tenant.id, name="Data Analysis", category="Analytical", description="Data analysis skills"),
        Skill(tenant_id=test_tenant.id, name="Communication", category="Interpersonal", description="Communication skills"),
    ]
    for skill in skills:
        db.add(skill)
    db.commit()
    for skill in skills:
        db.refresh(skill)
    return skills

@pytest.fixture
def test_courses(db, test_tenant, test_skills):
    courses = [
        Course(
            tenant_id=test_tenant.id,
            name="Introduction to Programming",
            course_code="COMP101",
            difficulty_level=0.3,
            term_offered="1"
        ),
        Course(
            tenant_id=test_tenant.id,
            name="Data Science",
            course_code="DATA301",
            difficulty_level=0.7,
            term_offered="4"
        ),
    ]
    for course in courses:
        db.add(course)
    db.commit()
    
    for course in courses:
        db.refresh(course)
        for skill in test_skills[:2]:
            rel = SkillRelationship(skill_id=skill.id, course_id=course.id, confidence_level=0.8)
            db.add(rel)
    db.commit()
    
    return courses

@pytest.fixture
def test_role_cluster(db, test_tenant):
    role = RoleCluster(
        tenant_id=test_tenant.id,
        name="Software Engineering Roles",
        description="Building software systems",
        skill_weights={
            "Python Programming": 0.85,
            "Data Analysis": 0.70,
            "Communication": 0.60
        },
        psychometric_ranges={
            "decision_style": [0.6, 1.0],
            "risk_tolerance": [0.4, 0.8],
            "structure_preference": [0.5, 0.9],
            "social_preference": [0.3, 0.7],
            "feedback_sensitivity": [0.5, 1.0]
        },
        example_careers=["Software Engineer", "Developer"],
        typical_pathways=["CS degree"]
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role
