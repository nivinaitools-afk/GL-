# GetLanded Career Intelligence Backend

A FastAPI-based career guidance system that matches students to career paths using psychometric profiling and skill analysis.

## Features

- **Multi-tenant architecture** - Supports multiple universities with data isolation
- **Psychometric profiling** - Maps scenario-based assessments to 5-dimensional personality profiles
- **Career matching** - Intelligent role matching using psychometric fit (40%) and skill readiness (60%)
- **Dynamic roadmaps** - Personalized course recommendations to bridge skill gaps
- **UK-focused seed data** - 50 skills, 40 courses, 15 role clusters

## Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── database/
│   │   ├── config.py          # Database configuration
│   │   └── models.py          # SQLAlchemy ORM models
│   ├── schemas/               # Pydantic schemas
│   ├── routers/               # API route handlers
│   ├── engines/               # Core logic
│   │   ├── psychometric_engine.py
│   │   ├── role_matcher.py
│   │   └── roadmap_generator.py
│   └── utils/                 # Utility functions
├── seeds/                     # Seed data
└── tests/                     # Test suite
```

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 12+

### Installation

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure database:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Create database:**
```bash
createdb getlanded
```

4. **Load seed data:**
```bash
python seeds/load_seeds.py
```

This will create:
- A default tenant (University of Example)
- 50 skills across Technical, Analytical, Interpersonal, Leadership, and Business categories
- 40 UK university courses
- 15 role clusters with psychometric ranges and skill requirements

5. **Start the server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Interactive documentation at `http://localhost:8000/docs`

## API Endpoints

### Tenants
- `POST /tenants` - Create university tenant
- `GET /tenants/{id}` - Get tenant configuration

### Students
- `POST /students` - Create student
- `GET /students/{id}` - Get student profile
- `PUT /students/{id}` - Update student

### Psychometrics
- `POST /students/{id}/psychometrics` - Submit assessment responses
- `GET /students/{id}/psychometrics` - Get psychometric profile

### Career Intelligence
- `GET /students/{id}/career-matches` - Get ranked career matches
- `POST /students/{id}/roadmap` - Generate career roadmap
- `GET /students/{id}/roadmap/{version}` - Retrieve specific roadmap

### Reference Data
- `GET /role-clusters?tenant_id={id}` - List all role clusters
- `GET /skills?tenant_id={id}` - List all skills
- `GET /courses?tenant_id={id}` - List all courses
- `GET /health` - Health check

## Usage Examples

### 1. Create a Student

```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "university": "University of Example",
    "graduation_year": 2025
  }'
```

### 2. Submit Psychometric Assessment

```bash
curl -X POST "http://localhost:8000/students/1/psychometrics" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": {
      "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
      "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
      "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
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

### 3. Get Career Matches

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
    "explanation": "You have an excellent personality fit (92%) and strong skill readiness (84%) for Software Engineering Roles...",
    "skill_gaps": [],
    "example_careers": ["Software Engineer", "Backend Developer"]
  }
]
```

### 4. Generate Career Roadmap

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
  "overall_narrative": "Based on your profile, you're currently at 65% fit for Data Science & Analytics Roles...",
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
        }
      ],
      "focus_areas": ["Statistical Analysis", "Data Analysis"],
      "rationale": "Build foundational skills in Statistical Analysis, Data Analysis to establish a strong base."
    }
  ]
}
```

## Database Schema

### Core Tables

- **tenants** - University/organization configuration
- **students** - Student profiles
- **psychometric_profiles** - 5D psychometric vectors
- **skills** - Skills taxonomy (Technical, Analytical, Interpersonal, Leadership, Business)
- **role_clusters** - Career role groupings with requirements
- **courses** - University courses
- **skill_relationships** - Course-skill mappings
- **student_skills** - Student skill proficiency levels
- **career_roadmaps** - Generated roadmap versions

All tables include `tenant_id` for multi-tenant isolation.

## Testing

Run the test suite:

```bash
cd backend
pytest -v
```

Test coverage includes:
- ✅ Psychometric scoring and normalization
- ✅ Role matching algorithms
- ✅ Roadmap generation logic
- ✅ API endpoints
- ✅ End-to-end flow (student → psychometrics → matches → roadmap)

## Algorithms

### Psychometric Engine

Maps 8-12 scenario questions (1-5 scale) to 5 dimensions:
- **Decision Style**: Analytical vs. Intuitive (0-1)
- **Risk Tolerance**: Risk-seeking vs. Risk-averse (0-1)
- **Structure Preference**: Structured vs. Flexible (0-1)
- **Social Preference**: Collaborative vs. Independent (0-1)
- **Feedback Sensitivity**: Feedback-seeking vs. Self-directed (0-1)

### Role Matcher

**Fit Score** = 0.4 × Psychometric Fit + 0.6 × Skill Readiness

- **Psychometric Fit**: How well student's profile matches role's acceptable ranges
- **Skill Readiness**: Weighted average of student's proficiency vs. required levels

### Roadmap Generator

1. Identify skill gaps (required - current > threshold)
2. Find courses that teach gap skills
3. Rank courses by impact (gap size × course confidence)
4. Distribute courses across terms
5. Calculate projected improvement

## Seed Data

### Skills (50 total)
- **Technical**: Python, Java, JavaScript, SQL, Machine Learning, Cloud Computing, DevOps, etc.
- **Analytical**: Data Analysis, Statistical Analysis, Research Methods, Critical Thinking, etc.
- **Interpersonal**: Communication, Teamwork, Stakeholder Management, Negotiation, etc.
- **Leadership**: Project Management, Leadership, Strategic Thinking, Change Management, etc.
- **Business**: Financial Analysis, Marketing, Operations Management, Business Strategy, etc.

### Courses (40 total)
UK 3-year degree structure across:
- Computer Science (COMP101-350)
- Mathematics & Data (MATH201-202, DATA301-310)
- Economics (ECON101-102)
- Finance & Accounting (FIN201-301, ACCT101-201)
- Management (MGMT210-320)
- Others (Marketing, Design, Research, etc.)

### Role Clusters (15 total)
1. Software Engineering Roles
2. Data Science & Analytics Roles
3. Product Management Roles
4. Business Strategy & Consulting Roles
5. Finance & Quantitative Roles
6. Operations & Supply Chain Roles
7. Marketing & Growth Roles
8. Research & Academic Roles
9. UX/UI Design Roles
10. DevOps & Cloud Engineering Roles
11. Leadership & Management Roles
12. Cybersecurity Roles
13. Entrepreneurship & Startup Roles
14. Project Management Roles
15. Quality Assurance & Testing Roles

## Multi-Tenant Design

All data is isolated by `tenant_id`. Single API instance serves multiple universities with:
- Separate skill taxonomies
- Custom course catalogs
- University-specific role clusters
- Isolated student data

## Development

### Adding New Role Clusters

Edit `seeds/role_clusters.json`:

```json
{
  "name": "New Role Cluster",
  "description": "Description of role",
  "skill_weights": {
    "Skill Name": 0.85
  },
  "psychometric_ranges": {
    "decision_style": [0.6, 1.0]
  },
  "example_careers": ["Job Title 1", "Job Title 2"],
  "typical_pathways": ["Pathway description"]
}
```

### Adding New Skills

Edit `seeds/skills.json`:

```json
{
  "name": "New Skill",
  "category": "Technical|Analytical|Interpersonal|Leadership|Business",
  "description": "Skill description"
}
```

### Adding New Courses

Edit `seeds/courses.json`:

```json
{
  "name": "Course Name",
  "course_code": "DEPT###",
  "difficulty_level": 0.7,
  "term_offered": "3",
  "description": "Course description",
  "skills": ["Skill 1", "Skill 2"]
}
```

## Production Deployment

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@host:5432/getlanded
SECRET_KEY=your-secret-key
DEBUG=False
```

## License

MIT

## Support

For questions or issues, please open a GitHub issue.
