import pytest
from app.engines.roadmap_generator import RoadmapGenerator

def test_identify_skill_gaps():
    """Test skill gap identification."""
    student_skills = {
        "Python Programming": 0.5,
        "Data Analysis": 0.3
    }
    
    required_skills = {
        "Python Programming": 0.85,
        "Data Analysis": 0.80,
        "Communication": 0.70
    }
    
    gaps = RoadmapGenerator.identify_skill_gaps(student_skills, required_skills, threshold=0.15)
    
    assert len(gaps) > 0
    
    gap_skills = [g["skill"] for g in gaps]
    assert "Python Programming" in gap_skills
    assert "Data Analysis" in gap_skills
    assert "Communication" in gap_skills
    
    for gap in gaps:
        assert "skill" in gap
        assert "current" in gap
        assert "required" in gap
        assert "gap" in gap
        assert "priority" in gap

def test_skill_gaps_prioritization():
    """Test that skill gaps are prioritized correctly."""
    student_skills = {"Skill A": 0.2, "Skill B": 0.6}
    required_skills = {"Skill A": 0.9, "Skill B": 0.8}
    
    gaps = RoadmapGenerator.identify_skill_gaps(student_skills, required_skills)
    
    assert gaps[0]["skill"] == "Skill A"
    assert gaps[0]["gap"] > gaps[1]["gap"]

def test_calculate_projected_improvement():
    """Test projected improvement calculation."""
    skill_gaps = [
        {"skill": "Python Programming", "gap": 0.4},
        {"skill": "Data Analysis", "gap": 0.5},
        {"skill": "Communication", "gap": 0.3}
    ]
    
    term_plan = [
        {"term": 1, "focus_areas": ["Python Programming", "Data Analysis"]},
        {"term": 2, "focus_areas": ["Communication"]}
    ]
    
    improvement = RoadmapGenerator.calculate_projected_improvement(skill_gaps, term_plan)
    
    assert 0.0 <= improvement <= 1.0
    assert improvement > 0

def test_generate_narrative():
    """Test narrative generation."""
    skill_gaps = [
        {"skill": "Python Programming", "gap": 0.4},
        {"skill": "Data Analysis", "gap": 0.3}
    ]
    
    narrative = RoadmapGenerator.generate_narrative(
        "Test Student",
        "Software Engineering Roles",
        0.5,
        0.8,
        skill_gaps
    )
    
    assert isinstance(narrative, str)
    assert len(narrative) > 0
    assert "Software Engineering Roles" in narrative

def test_recommend_courses(db, test_tenant, test_courses, test_skills):
    """Test course recommendation."""
    skill_gaps = [
        {"skill": "Python Programming", "gap": 0.5, "priority": "high"},
        {"skill": "Data Analysis", "gap": 0.4, "priority": "high"}
    ]
    
    term_plan = RoadmapGenerator.recommend_courses(
        db,
        test_tenant.id,
        skill_gaps,
        time_horizon_terms=4
    )
    
    assert isinstance(term_plan, list)
    assert len(term_plan) > 0
    
    for term in term_plan:
        assert "term" in term
        assert "courses" in term
        assert "focus_areas" in term
        assert "rationale" in term

def test_roadmap_api(client, test_student, test_role_cluster, test_skills, test_courses, db):
    """Test roadmap generation API endpoint."""
    from app.database.models import StudentSkill
    
    for skill in test_skills:
        student_skill = StudentSkill(
            student_id=test_student.id,
            skill_id=skill.id,
            proficiency_level=0.4,
            source="explicit"
        )
        db.add(student_skill)
    
    db.commit()
    
    request_data = {
        "target_role_cluster_id": test_role_cluster.id,
        "time_horizon_terms": 4
    }
    
    response = client.post(f"/students/{test_student.id}/roadmap", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "overall_narrative" in data
    assert "target_role" in data
    assert "current_fit_score" in data
    assert "projected_fit_score" in data
    assert "skill_gaps" in data
    assert "term_by_term" in data
    
    assert isinstance(data["skill_gaps"], list)
    assert isinstance(data["term_by_term"], list)
    assert 0.0 <= data["current_fit_score"] <= 1.0
    assert 0.0 <= data["projected_fit_score"] <= 1.0

def test_get_roadmap(client, test_student, test_role_cluster, test_skills, test_courses, db):
    """Test retrieving a roadmap."""
    from app.database.models import StudentSkill
    
    for skill in test_skills:
        student_skill = StudentSkill(
            student_id=test_student.id,
            skill_id=skill.id,
            proficiency_level=0.4,
            source="explicit"
        )
        db.add(student_skill)
    
    db.commit()
    
    request_data = {
        "target_role_cluster_id": test_role_cluster.id,
        "time_horizon_terms": 4
    }
    
    create_response = client.post(f"/students/{test_student.id}/roadmap", json=request_data)
    assert create_response.status_code == 200
    
    get_response = client.get(f"/students/{test_student.id}/roadmap/1")
    
    assert get_response.status_code == 200
    data = get_response.json()
    
    assert "overall_narrative" in data
    assert "target_role" in data
