import pytest
from app.engines.psychometric_engine import PsychometricEngine

def test_normalize_response():
    """Test response normalization."""
    assert PsychometricEngine.normalize_response(1) == 0.0
    assert PsychometricEngine.normalize_response(3) == 0.5
    assert PsychometricEngine.normalize_response(5) == 1.0
    
    assert PsychometricEngine.normalize_response(5, invert=True) == 0.0
    assert PsychometricEngine.normalize_response(1, invert=True) == 1.0

def test_calculate_profile():
    """Test psychometric profile calculation."""
    responses = {
        "Q1": 5,
        "Q2": 2,
        "Q3": 4,
        "Q4": 5,
        "Q5": 4,
        "Q6": 2,
        "Q7": 5,
        "Q8": 4,
        "Q9": 3,
        "Q10": 3,
        "Q11": 5,
        "Q12": 2
    }
    
    profile = PsychometricEngine.calculate_profile(responses)
    
    assert "decision_style" in profile
    assert "risk_tolerance" in profile
    assert "structure_preference" in profile
    assert "social_preference" in profile
    assert "feedback_sensitivity" in profile
    
    for dimension, score in profile.items():
        assert 0.0 <= score <= 1.0, f"{dimension} score {score} out of range"

def test_partial_responses():
    """Test handling of partial responses."""
    responses = {"Q1": 4, "Q3": 5}
    profile = PsychometricEngine.calculate_profile(responses)
    
    assert all(0.0 <= score <= 1.0 for score in profile.values())

def test_consistent_calculation():
    """Test that same responses give same profile."""
    responses = {"Q1": 4, "Q2": 3, "Q3": 5, "Q4": 2}
    
    profile1 = PsychometricEngine.calculate_profile(responses)
    profile2 = PsychometricEngine.calculate_profile(responses)
    
    assert profile1 == profile2

def test_psychometric_api(client, test_student):
    """Test psychometric API endpoint."""
    responses = {
        "responses": {
            "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
            "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
            "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
        }
    }
    
    response = client.post(f"/students/{test_student.id}/psychometrics", json=responses)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "decision_style" in data
    assert "risk_tolerance" in data
    assert 0.0 <= data["decision_style"] <= 1.0
    assert 0.0 <= data["risk_tolerance"] <= 1.0

def test_get_psychometric_profile(client, test_student):
    """Test retrieving psychometric profile."""
    responses = {
        "responses": {
            "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
            "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
            "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
        }
    }
    
    client.post(f"/students/{test_student.id}/psychometrics", json=responses)
    
    response = client.get(f"/students/{test_student.id}/psychometrics")
    
    assert response.status_code == 200
    data = response.json()
    assert "student_id" in data
    assert data["student_id"] == test_student.id
