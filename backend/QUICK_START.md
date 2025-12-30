# GetLanded Backend - Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+

### Installation

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
createdb getlanded

# 5. Configure environment
cp .env.example .env
# Edit .env if needed (default settings work for local PostgreSQL)

# 6. Load seed data
python seeds/load_seeds.py

# 7. Run tests
pytest -v

# 8. Start server
./run.sh
# or: uvicorn app.main:app --reload
```

### Access
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

## 📝 First API Call

```bash
# Get health status
curl http://localhost:8000/health

# List all role clusters
curl "http://localhost:8000/role-clusters?tenant_id=1"

# Create a student
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "name": "Test Student",
    "email": "test@example.com",
    "graduation_year": 2025
  }'
```

---

## 🎯 Complete Flow Example

```bash
# 1. Create student
STUDENT_ID=$(curl -s -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "graduation_year": 2025
  }' | jq -r '.id')

echo "Created student with ID: $STUDENT_ID"

# 2. Submit psychometric assessment
curl -X POST "http://localhost:8000/students/$STUDENT_ID/psychometrics" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": {
      "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
      "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
      "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
    }
  }' | jq

# 3. Get career matches
curl "http://localhost:8000/students/$STUDENT_ID/career-matches" | jq

# 4. Generate roadmap (use first match's role_cluster_id)
ROLE_ID=$(curl -s "http://localhost:8000/students/$STUDENT_ID/career-matches" | jq -r '.[0].role_cluster_id')

curl -X POST "http://localhost:8000/students/$STUDENT_ID/roadmap" \
  -H "Content-Type: application/json" \
  -d "{
    \"target_role_cluster_id\": $ROLE_ID,
    \"time_horizon_terms\": 4
  }" | jq
```

---

## 🧪 Running Tests

```bash
# All tests
pytest -v

# Specific test file
pytest tests/test_psychometric.py -v

# With coverage
pytest --cov=app tests/

# Quick test (no verbose)
pytest -q
```

**Expected Output:**
```
======================== 24 passed in 1.86s ========================
```

---

## 📊 Project Structure

```
backend/
├── app/                        # Application code
│   ├── main.py                # FastAPI app
│   ├── database/              # DB config & models
│   ├── schemas/               # Pydantic schemas
│   ├── routers/               # API endpoints
│   ├── engines/               # Core logic
│   └── utils/                 # Helper functions
├── seeds/                      # Seed data
│   ├── skills.json            # 50 skills
│   ├── courses.json           # 40 courses
│   ├── role_clusters.json     # 15 role clusters
│   └── load_seeds.py          # Loader script
├── tests/                      # Test suite (24 tests)
└── requirements.txt            # Dependencies
```

---

## 🔧 Common Commands

### Database
```bash
# Create database
createdb getlanded

# Drop database
dropdb getlanded

# Connect to database
psql getlanded

# Reload seed data
python seeds/load_seeds.py
```

### Development
```bash
# Start server (hot reload)
uvicorn app.main:app --reload

# Start on different port
uvicorn app.main:app --reload --port 8080

# Run tests
pytest -v

# Run specific test
pytest tests/test_psychometric.py::test_normalize_response -v
```

### Debugging
```bash
# Check if server is running
curl http://localhost:8000/health

# View logs
# (logs printed to console when running with --reload)

# Check PostgreSQL connection
psql -U postgres -d getlanded -c "SELECT COUNT(*) FROM students;"
```

---

## 📚 Documentation

- **Full README**: [README.md](README.md)
- **API Examples**: [API_EXAMPLES.md](API_EXAMPLES.md)
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Task Completion**: [TASK_COMPLETION.md](TASK_COMPLETION.md)

---

## 🐛 Troubleshooting

### Port already in use
```bash
lsof -i :8000
kill -9 <PID>
```

### Database connection error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Verify connection
psql -U postgres -d getlanded
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python  # Should point to venv/bin/python
```

### Tests failing
```bash
# Ensure using test database
export DATABASE_URL=sqlite:///./test.db
pytest -v
```

---

## 💡 Next Steps

1. ✅ Explore API docs: http://localhost:8000/docs
2. ✅ Try example API calls above
3. ✅ Read [API_EXAMPLES.md](API_EXAMPLES.md) for more
4. ✅ Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture
5. ✅ Review [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

---

## ✅ What's Working

- ✅ 15 API endpoints fully functional
- ✅ Psychometric profiling (5D personality model)
- ✅ Career matching (15 role clusters)
- ✅ Roadmap generation (course recommendations)
- ✅ Multi-tenant support (tenant_id: 1)
- ✅ All 24 tests passing
- ✅ Interactive API documentation

---

## 🎯 Key Endpoints

```
Health:     GET    /health
Students:   POST   /students
            GET    /students/{id}
Psych:      POST   /students/{id}/psychometrics
            GET    /students/{id}/psychometrics
Matches:    GET    /students/{id}/career-matches
Roadmaps:   POST   /students/{id}/roadmap
            GET    /students/{id}/roadmap/{version}
Reference:  GET    /role-clusters?tenant_id=1
            GET    /skills?tenant_id=1
            GET    /courses?tenant_id=1
```

**Status**: Ready for pilot deployment 🚀
