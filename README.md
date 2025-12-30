# GetLanded - Career Intelligence Platform

An AI-powered career guidance platform that matches students to career paths using psychometric profiling and skill analysis.

## Project Structure

```
getlanded/
├── backend/              # Python FastAPI backend (Phase 1 - Complete ✅)
│   ├── app/             # Application code
│   ├── seeds/           # Seed data (50 skills, 40 courses, 15 role clusters)
│   ├── tests/           # Test suite (24 tests, all passing)
│   └── README.md        # Backend documentation
│
└── frontend/            # Next.js frontend (Future Phase)
    └── app/             # React components
```

## Quick Start

### Backend API (Phase 1 - Production Ready)

The backend is a fully functional FastAPI service that:
- ✅ Profiles students using psychometric assessments
- ✅ Matches students to 15 UK-relevant career clusters
- ✅ Generates personalized 4-term career roadmaps
- ✅ Supports multi-tenant architecture for universities

**Setup:**
```bash
cd backend

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
createdb getlanded
cp .env.example .env
# Edit .env with your database credentials

# Load seed data
python seeds/load_seeds.py

# Run tests
pytest -v

# Start server
./run.sh
```

**Access:**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- API examples: See `backend/API_EXAMPLES.md`

**Full Documentation:**
- [Backend README](backend/README.md) - Complete setup & usage guide
- [API Examples](backend/API_EXAMPLES.md) - Curl commands & Python examples
- [Project Summary](backend/PROJECT_SUMMARY.md) - Architecture & features
- [Deployment Guide](backend/DEPLOYMENT.md) - Production deployment

### Frontend (Future Phase)

The frontend will be built with Next.js and will include:
- Interactive psychometric assessment interface
- Visual career match dashboard
- Animated roadmap timeline
- Student profile management

**Planned Setup:**
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the frontend (once built).

## Features (Phase 1 - Backend)

### 🎯 Psychometric Profiling
- 12 scenario-based questions (1-5 scale)
- Maps to 5-dimensional personality profile:
  - Decision Style (Analytical vs. Intuitive)
  - Risk Tolerance (Risk-seeking vs. Risk-averse)
  - Structure Preference (Structured vs. Flexible)
  - Social Preference (Collaborative vs. Independent)
  - Feedback Sensitivity (Feedback-seeking vs. Self-directed)

### 🎓 Career Matching
- **Fit Score = 0.4 × Psychometric Fit + 0.6 × Skill Readiness**
- Matches to 15 role clusters:
  - Software Engineering
  - Data Science & Analytics
  - Product Management
  - Business Strategy & Consulting
  - Finance & Quantitative Roles
  - Operations & Supply Chain
  - Marketing & Growth
  - Research & Academic
  - UX/UI Design
  - DevOps & Cloud Engineering
  - Leadership & Management
  - Cybersecurity
  - Entrepreneurship & Startup
  - Project Management
  - Quality Assurance & Testing

### 🗺️ Dynamic Roadmaps
- Identifies skill gaps vs. target role requirements
- Recommends courses from 40 UK university courses
- 4-term planning horizon
- Projects improvement: Current fit → Projected fit
- Explainable AI with natural language rationales

### 🏫 Multi-Tenant Architecture
- University-level data isolation
- Supports unlimited universities
- Customizable skill taxonomies per tenant
- UK-first, ready for international expansion

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 12+ (SQLite for tests)
- **ORM**: SQLAlchemy 2.0.25
- **Testing**: pytest 7.4.4
- **Python**: 3.9+

### Frontend (Planned)
- **Framework**: Next.js 14
- **UI**: React + TypeScript
- **Styling**: Tailwind CSS
- **State**: React Context / Zustand

## API Endpoints

### Core Functionality
- `POST /tenants` - Create university tenant
- `POST /students` - Create student
- `POST /students/{id}/psychometrics` - Submit assessment
- `GET /students/{id}/career-matches` - Get ranked matches
- `POST /students/{id}/roadmap` - Generate roadmap

### Reference Data
- `GET /role-clusters?tenant_id={id}` - List role clusters
- `GET /skills?tenant_id={id}` - List skills
- `GET /courses?tenant_id={id}` - List courses
- `GET /health` - Health check

See [API_EXAMPLES.md](backend/API_EXAMPLES.md) for detailed usage.

## Testing

```bash
cd backend
pytest -v
```

**Results:**
```
============================= test session starts ==============================
collected 24 items

tests/test_e2e.py::test_complete_flow PASSED                             [  4%]
tests/test_e2e.py::test_reference_data_endpoints PASSED                  [  8%]
tests/test_e2e.py::test_health_check PASSED                              [ 12%]
tests/test_e2e.py::test_root_endpoint PASSED                             [ 16%]
tests/test_psychometric.py (6 tests) PASSED                              [ 41%]
tests/test_roadmap.py (7 tests) PASSED                                   [ 70%]
tests/test_role_matcher.py (7 tests) PASSED                              [100%]

======================= 24 passed, 32 warnings in 1.69s ========================
```

## Development Roadmap

### ✅ Phase 1: Backend Core (Complete)
- [x] Database schema & models
- [x] Psychometric engine
- [x] Role matcher algorithm
- [x] Roadmap generator
- [x] REST API endpoints
- [x] Seed data (50 skills, 40 courses, 15 roles)
- [x] Comprehensive tests
- [x] Documentation

### 🔄 Phase 2: Frontend (Next)
- [ ] Student portal UI
- [ ] Interactive psychometric assessment
- [ ] Career match dashboard
- [ ] Roadmap visualization
- [ ] Profile management

### 📋 Phase 3: Advanced Features
- [ ] Real job posting integration (LinkedIn, Indeed)
- [ ] ML-based skill inference
- [ ] Collaborative filtering
- [ ] Industry trend analysis
- [ ] Admin dashboard for universities

### 🚀 Phase 4: Production
- [ ] Alembic migrations
- [ ] Redis caching
- [ ] Background jobs
- [ ] Advanced analytics
- [ ] Mobile app

## Example Flow

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Create student
student = requests.post(f"{BASE_URL}/students", json={
    "tenant_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "graduation_year": 2025
}).json()

# 2. Submit psychometric assessment
profile = requests.post(
    f"{BASE_URL}/students/{student['id']}/psychometrics",
    json={"responses": {"Q1": 5, "Q2": 2, ..., "Q12": 2}}
).json()
# → {"decision_style": 0.85, "risk_tolerance": 0.72, ...}

# 3. Get career matches
matches = requests.get(
    f"{BASE_URL}/students/{student['id']}/career-matches"
).json()
# → [{"name": "Software Engineering Roles", "fit_score": 0.87, ...}, ...]

# 4. Generate roadmap
roadmap = requests.post(
    f"{BASE_URL}/students/{student['id']}/roadmap",
    json={"target_role_cluster_id": matches[0]["role_cluster_id"], "time_horizon_terms": 4}
).json()
# → {"current_fit_score": 0.65, "projected_fit_score": 0.89, "term_by_term": [...]}
```

## Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and add tests
4. Ensure all tests pass: `pytest -v`
5. Submit a pull request

### Code Style
- Python: Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Add tests for new features

## License

MIT

## Support

- Documentation: http://localhost:8000/docs (when running)
- Issues: [GitHub Issues](https://github.com/your-org/getlanded/issues)
- Email: support@getlanded.com

---

## Current Status

**Backend (Phase 1)**: ✅ Production-ready
- All core features implemented
- 24 tests passing
- Comprehensive documentation
- Ready for frontend integration

**Frontend**: 📋 Planned for Phase 2

The GetLanded backend is ready for pilot deployment with a university partner. See [PROJECT_SUMMARY.md](backend/PROJECT_SUMMARY.md) for detailed feature breakdown.
