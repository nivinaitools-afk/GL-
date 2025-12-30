# GetLanded API Examples

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example API Flow

### 1. Create a Tenant (University)

```bash
curl -X POST "http://localhost:8000/tenants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "University of Example",
    "country": "UK",
    "branding_config": {"primary_color": "#003366"}
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "University of Example",
  "country": "UK",
  "branding_config": {"primary_color": "#003366"},
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Create a Student

```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "university": "University of Example",
    "graduation_year": 2025
  }'
```

**Response:**
```json
{
  "id": 1,
  "tenant_id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "university": "University of Example",
  "graduation_year": 2025,
  "created_at": "2024-01-15T10:31:00"
}
```

### 3. Submit Psychometric Assessment

```bash
curl -X POST "http://localhost:8000/students/1/psychometrics" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": {
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
  }'
```

**Response:**
```json
{
  "decision_style": 0.85,
  "risk_tolerance": 0.72,
  "structure_preference": 0.78,
  "social_preference": 0.81,
  "feedback_sensitivity": 0.50
}
```

**Question Guide:**
- **Q1-Q2, Q11**: Decision Style (analytical vs. intuitive)
- **Q3-Q4, Q12**: Risk Tolerance (risk-seeking vs. risk-averse)
- **Q5-Q6**: Structure Preference (structured vs. flexible)
- **Q7-Q8**: Social Preference (collaborative vs. independent)
- **Q9-Q10**: Feedback Sensitivity (feedback-seeking vs. self-directed)

Scale: 1 (Strongly Disagree) to 5 (Strongly Agree)

### 4. Get Career Matches

```bash
curl "http://localhost:8000/students/1/career-matches"
```

**Response:**
```json
[
  {
    "role_cluster_id": 1,
    "name": "Software Engineering Roles",
    "description": "Building and maintaining software systems",
    "fit_score": 0.87,
    "psychometric_fit": 0.92,
    "skill_readiness": 0.84,
    "explanation": "You have an excellent personality fit (92%) and strong skill readiness (84%) for Software Engineering Roles. Key areas to develop: System Design, API Development.",
    "skill_gaps": [
      {
        "skill": "System Design",
        "current": 0.60,
        "required": 0.80,
        "gap": 0.20
      }
    ],
    "example_careers": [
      "Software Engineer",
      "Backend Developer",
      "Full Stack Developer"
    ]
  },
  {
    "role_cluster_id": 2,
    "name": "Data Science & Analytics Roles",
    "description": "Extracting insights from data",
    "fit_score": 0.82,
    "psychometric_fit": 0.89,
    "skill_readiness": 0.78,
    "explanation": "You have an excellent personality fit (89%) and strong skill readiness (78%) for Data Science & Analytics Roles. Key areas to develop: Machine Learning, Statistical Analysis.",
    "skill_gaps": [
      {
        "skill": "Machine Learning",
        "current": 0.40,
        "required": 0.75,
        "gap": 0.35
      }
    ],
    "example_careers": [
      "Data Scientist",
      "Data Analyst",
      "ML Engineer"
    ]
  }
]
```

### 5. Generate Career Roadmap

```bash
curl -X POST "http://localhost:8000/students/1/roadmap" \
  -H "Content-Type: application/json" \
  -d '{
    "target_role_cluster_id": 2,
    "time_horizon_terms": 4
  }'
```

**Response:**
```json
{
  "overall_narrative": "Based on your profile, you're currently at 65% fit for Data Science & Analytics Roles. You have a solid foundation to build upon. Your primary focus areas are: Machine Learning, Statistical Analysis, Data Visualization. Following this roadmap can increase your fit to 89%, a 24% improvement over 5 key skill areas.",
  "target_role": "Data Science & Analytics Roles",
  "current_fit_score": 0.65,
  "projected_fit_score": 0.89,
  "skill_gaps": [
    {
      "skill": "Machine Learning",
      "current": 0.30,
      "required": 0.75,
      "gap": 0.45,
      "priority": "high"
    },
    {
      "skill": "Statistical Analysis",
      "current": 0.50,
      "required": 0.90,
      "gap": 0.40,
      "priority": "high"
    },
    {
      "skill": "Data Visualization",
      "current": 0.60,
      "required": 0.85,
      "gap": 0.25,
      "priority": "low"
    }
  ],
  "term_by_term": [
    {
      "term": 1,
      "courses": [
        {
          "course_code": "MATH201",
          "course_name": "Statistics for Data Science",
          "skills_developed": ["Statistical Analysis", "Data Analysis"],
          "impact": 0.85,
          "difficulty": 0.7
        },
        {
          "course_code": "COMP210",
          "course_name": "Database Systems",
          "skills_developed": ["SQL", "Data Analysis"],
          "impact": 0.72,
          "difficulty": 0.6
        }
      ],
      "focus_areas": ["Statistical Analysis", "Data Analysis", "SQL"],
      "rationale": "Build foundational skills in Statistical Analysis, Data Analysis to establish a strong base."
    },
    {
      "term": 2,
      "courses": [
        {
          "course_code": "DATA301",
          "course_name": "Data Science",
          "skills_developed": ["Data Analysis", "Data Visualization", "Python Programming"],
          "impact": 0.78,
          "difficulty": 0.8
        },
        {
          "course_code": "COMP301",
          "course_name": "Machine Learning",
          "skills_developed": ["Machine Learning", "Python Programming", "Statistical Analysis"],
          "impact": 0.91,
          "difficulty": 0.8
        }
      ],
      "focus_areas": ["Machine Learning", "Data Visualization", "Python Programming"],
      "rationale": "Deepen expertise in Machine Learning, Data Visualization while maintaining momentum."
    }
  ]
}
```

### 6. Retrieve Saved Roadmap

```bash
curl "http://localhost:8000/students/1/roadmap/1"
```

Returns the same format as above for a specific version.

### 7. List All Student Roadmaps

```bash
curl "http://localhost:8000/students/1/roadmaps"
```

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "version": 1,
    "role_cluster_id": 2,
    "recommendations": { ... },
    "generated_at": "2024-01-15T10:35:00"
  }
]
```

## Reference Data Endpoints

### Get All Role Clusters

```bash
curl "http://localhost:8000/role-clusters?tenant_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Software Engineering Roles",
    "description": "Building and maintaining software systems",
    "example_careers": [
      "Software Engineer",
      "Backend Developer",
      "Full Stack Developer"
    ]
  },
  {
    "id": 2,
    "name": "Data Science & Analytics Roles",
    "description": "Extracting insights from data",
    "example_careers": [
      "Data Scientist",
      "Data Analyst",
      "ML Engineer"
    ]
  }
]
```

### Get All Skills

```bash
curl "http://localhost:8000/skills?tenant_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Python Programming",
    "category": "Technical",
    "description": "Proficiency in Python programming language"
  },
  {
    "id": 2,
    "name": "Data Analysis",
    "category": "Analytical",
    "description": "Analyzing and interpreting complex data"
  }
]
```

### Get Skills by Category

```bash
curl "http://localhost:8000/skills?tenant_id=1&category=Technical"
```

### Get All Courses

```bash
curl "http://localhost:8000/courses?tenant_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Introduction to Programming",
    "course_code": "COMP101",
    "difficulty_level": 0.3,
    "term_offered": "1",
    "description": "Foundational programming concepts using Python"
  }
]
```

## Health Check

```bash
curl "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "service": "GetLanded Career Intelligence API"
}
```

## Python Examples

### Using requests library

```python
import requests

BASE_URL = "http://localhost:8000"

# Create student
student_data = {
    "tenant_id": 1,
    "name": "Bob Smith",
    "email": "bob@example.com",
    "university": "University of Example",
    "graduation_year": 2025
}
response = requests.post(f"{BASE_URL}/students", json=student_data)
student = response.json()
student_id = student["id"]

# Submit psychometric assessment
psychometric_data = {
    "responses": {
        "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
        "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
        "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
    }
}
response = requests.post(
    f"{BASE_URL}/students/{student_id}/psychometrics",
    json=psychometric_data
)
profile = response.json()
print(f"Psychometric Profile: {profile}")

# Get career matches
response = requests.get(f"{BASE_URL}/students/{student_id}/career-matches")
matches = response.json()
print(f"Top Match: {matches[0]['name']} ({matches[0]['fit_score']:.2%})")

# Generate roadmap
roadmap_request = {
    "target_role_cluster_id": matches[0]["role_cluster_id"],
    "time_horizon_terms": 4
}
response = requests.post(
    f"{BASE_URL}/students/{student_id}/roadmap",
    json=roadmap_request
)
roadmap = response.json()
print(f"Roadmap: {roadmap['current_fit_score']:.2%} → {roadmap['projected_fit_score']:.2%}")
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Student not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```
