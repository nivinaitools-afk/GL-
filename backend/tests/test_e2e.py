import pytest

def test_complete_flow(client, test_tenant, test_skills, test_courses, test_role_cluster, db):
    """
    End-to-end test: student creation → psychometrics → matches → roadmap
    """
    
    student_data = {
        "tenant_id": test_tenant.id,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "university": "Test University",
        "graduation_year": 2025
    }
    
    student_response = client.post("/students", json=student_data)
    assert student_response.status_code == 200
    student = student_response.json()
    student_id = student["id"]
    
    psychometric_data = {
        "responses": {
            "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
            "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
            "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
        }
    }
    
    psych_response = client.post(
        f"/students/{student_id}/psychometrics",
        json=psychometric_data
    )
    assert psych_response.status_code == 200
    psychometric_profile = psych_response.json()
    assert "decision_style" in psychometric_profile
    
    from app.database.models import StudentSkill
    for skill in test_skills:
        student_skill = StudentSkill(
            student_id=student_id,
            skill_id=skill.id,
            proficiency_level=0.5,
            source="explicit"
        )
        db.add(student_skill)
    db.commit()
    
    matches_response = client.get(f"/students/{student_id}/career-matches")
    assert matches_response.status_code == 200
    matches = matches_response.json()
    assert len(matches) > 0
    assert "fit_score" in matches[0]
    
    best_match = matches[0]
    roadmap_request = {
        "target_role_cluster_id": best_match["role_cluster_id"],
        "time_horizon_terms": 4
    }
    
    roadmap_response = client.post(
        f"/students/{student_id}/roadmap",
        json=roadmap_request
    )
    assert roadmap_response.status_code == 200
    roadmap = roadmap_response.json()
    
    assert "overall_narrative" in roadmap
    assert "target_role" in roadmap
    assert "current_fit_score" in roadmap
    assert "projected_fit_score" in roadmap
    assert "skill_gaps" in roadmap
    assert "term_by_term" in roadmap
    
    assert roadmap["projected_fit_score"] >= roadmap["current_fit_score"]
    
    print("\n✅ Complete E2E flow successful!")
    print(f"   Student: {student['name']}")
    print(f"   Best Match: {best_match['name']} ({best_match['fit_score']:.2%})")
    print(f"   Roadmap: {roadmap['current_fit_score']:.2%} → {roadmap['projected_fit_score']:.2%}")

def test_reference_data_endpoints(client, test_tenant, test_skills, test_courses, test_role_cluster):
    """Test reference data endpoints."""
    
    skills_response = client.get(f"/skills?tenant_id={test_tenant.id}")
    assert skills_response.status_code == 200
    skills = skills_response.json()
    assert len(skills) > 0
    
    courses_response = client.get(f"/courses?tenant_id={test_tenant.id}")
    assert courses_response.status_code == 200
    courses = courses_response.json()
    assert len(courses) > 0
    
    roles_response = client.get(f"/role-clusters?tenant_id={test_tenant.id}")
    assert roles_response.status_code == 200
    roles = roles_response.json()
    assert len(roles) > 0

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
