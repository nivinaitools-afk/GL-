import pytest
from app.engines.role_matcher import RoleMatcher

def test_psychometric_fit_perfect_match():
    """Test psychometric fit with perfect match."""
    student_profile = {
        "decision_style": 0.8,
        "risk_tolerance": 0.6,
        "structure_preference": 0.7,
        "social_preference": 0.5,
        "feedback_sensitivity": 0.75
    }
    
    role_ranges = {
        "decision_style": [0.6, 1.0],
        "risk_tolerance": [0.4, 0.8],
        "structure_preference": [0.5, 0.9],
        "social_preference": [0.3, 0.7],
        "feedback_sensitivity": [0.5, 1.0]
    }
    
    fit = RoleMatcher.calculate_psychometric_fit(student_profile, role_ranges)
    
    assert 0.8 <= fit <= 1.0, f"Perfect match should have high fit, got {fit}"

def test_psychometric_fit_poor_match():
    """Test psychometric fit with poor match."""
    student_profile = {
        "decision_style": 0.2,
        "risk_tolerance": 0.1,
        "structure_preference": 0.2,
        "social_preference": 0.9,
        "feedback_sensitivity": 0.3
    }
    
    role_ranges = {
        "decision_style": [0.7, 1.0],
        "risk_tolerance": [0.7, 1.0],
        "structure_preference": [0.7, 1.0],
        "social_preference": [0.0, 0.3],
        "feedback_sensitivity": [0.7, 1.0]
    }
    
    fit = RoleMatcher.calculate_psychometric_fit(student_profile, role_ranges)
    
    assert fit < 0.5, f"Poor match should have low fit, got {fit}"

def test_skill_readiness_full_skills():
    """Test skill readiness with all required skills."""
    student_skills = {
        "Python Programming": 0.9,
        "Data Analysis": 0.8,
        "Communication": 0.7
    }
    
    required_skills = {
        "Python Programming": 0.85,
        "Data Analysis": 0.70,
        "Communication": 0.60
    }
    
    readiness, gaps = RoleMatcher.calculate_skill_readiness(student_skills, required_skills)
    
    assert readiness > 0.8, f"High skill levels should give high readiness, got {readiness}"
    assert len(gaps) == 0, "Should have no gaps when all skills exceed requirements"

def test_skill_readiness_with_gaps():
    """Test skill readiness with skill gaps."""
    student_skills = {
        "Python Programming": 0.4,
        "Data Analysis": 0.3
    }
    
    required_skills = {
        "Python Programming": 0.85,
        "Data Analysis": 0.80,
        "Communication": 0.70
    }
    
    readiness, gaps = RoleMatcher.calculate_skill_readiness(student_skills, required_skills)
    
    assert readiness < 0.5, f"Low skill levels should give low readiness, got {readiness}"
    assert len(gaps) > 0, "Should have gaps when skills don't meet requirements"
    
    gap_skills = [g["skill"] for g in gaps]
    assert "Python Programming" in gap_skills
    assert "Data Analysis" in gap_skills
    assert "Communication" in gap_skills

def test_fit_score_calculation():
    """Test overall fit score calculation."""
    psychometric_fit = 0.8
    skill_readiness = 0.6
    
    fit_score = RoleMatcher.calculate_fit_score(psychometric_fit, skill_readiness)
    
    expected = 0.4 * 0.8 + 0.6 * 0.6
    assert abs(fit_score - expected) < 0.001, f"Expected {expected}, got {fit_score}"
    
    assert 0.0 <= fit_score <= 1.0

def test_generate_explanation():
    """Test explanation generation."""
    explanation = RoleMatcher.generate_explanation(
        "Software Engineering Roles",
        0.85,
        0.70,
        0.78,
        [{"skill": "Python Programming", "gap": 0.3}]
    )
    
    assert "Software Engineering Roles" in explanation
    assert len(explanation) > 0
    assert isinstance(explanation, str)

def test_career_matches_api(client, test_student, test_role_cluster, test_skills, db):
    """Test career matches API endpoint."""
    from app.database.models import PsychometricProfile, StudentSkill
    
    profile = PsychometricProfile(
        tenant_id=test_student.tenant_id,
        student_id=test_student.id,
        decision_style=0.8,
        risk_tolerance=0.6,
        structure_preference=0.7,
        social_preference=0.5,
        feedback_sensitivity=0.75
    )
    db.add(profile)
    
    for skill in test_skills:
        student_skill = StudentSkill(
            student_id=test_student.id,
            skill_id=skill.id,
            proficiency_level=0.7,
            source="explicit"
        )
        db.add(student_skill)
    
    db.commit()
    
    response = client.get(f"/students/{test_student.id}/career-matches")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) > 0
    
    match = data[0]
    assert "role_cluster_id" in match
    assert "name" in match
    assert "fit_score" in match
    assert "explanation" in match
    assert 0.0 <= match["fit_score"] <= 1.0
