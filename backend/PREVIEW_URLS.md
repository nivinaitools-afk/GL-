# GetLanded Backend - Preview URLs

## 🚀 Server is Running!

The GetLanded Career Intelligence Backend API is now live on port 8000.

---

## 📍 Key URLs

### Main Endpoints

| URL | Description |
|-----|-------------|
| **http://localhost:8000/preview** | 🎨 **Visual Preview Page** (Start Here!) |
| **http://localhost:8000/docs** | 📚 Interactive API Documentation (Swagger) |
| **http://localhost:8000/redoc** | 📖 Alternative API Documentation (ReDoc) |
| **http://localhost:8000/health** | ✅ Health Check |
| **http://localhost:8000/** | 🏠 API Root |

---

## 🎯 Quick Test Commands

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. List Role Clusters
```bash
curl "http://localhost:8000/role-clusters?tenant_id=1"
```

### 3. List Skills
```bash
curl "http://localhost:8000/skills?tenant_id=1"
```

### 4. List Courses
```bash
curl "http://localhost:8000/courses?tenant_id=1"
```

### 5. Create a Student
```bash
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

## 📊 Seed Data Loaded

- ✅ **1 Tenant**: University of Example (ID: 1)
- ✅ **50 Skills**: Technical, Analytical, Interpersonal, Leadership, Business
- ✅ **40 Courses**: UK university structure (3-year degree)
- ✅ **15 Role Clusters**: Software Engineering, Data Science, Product Management, etc.

---

## 🔥 Demo Script

Run the complete demo:
```bash
cd /home/engine/project/backend
./demo.sh
```

---

## 📝 Complete Flow Example

```bash
# 1. Create student
STUDENT_ID=$(curl -s -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":1,"name":"Alice","email":"alice@test.com","graduation_year":2025}' \
  | jq -r '.id')

# 2. Submit psychometric assessment
curl -X POST "http://localhost:8000/students/$STUDENT_ID/psychometrics" \
  -H "Content-Type: application/json" \
  -d '{"responses":{"Q1":5,"Q2":2,"Q3":4,"Q4":5,"Q5":4,"Q6":2,"Q7":5,"Q8":4,"Q9":3,"Q10":3,"Q11":5,"Q12":2}}'

# 3. Get psychometric profile
curl "http://localhost:8000/students/$STUDENT_ID/psychometrics"

# Note: Career matches and roadmaps require student skills to be set up first
```

---

## 🎨 Visual Preview

**Open in your browser:**
```
http://localhost:8000/preview
```

This shows:
- ✅ API Status
- 📊 Seed Data Statistics
- 🚀 Available Endpoints
- 📖 Documentation Links
- 💡 Quick Start Examples

---

## 📚 Documentation Files

All in `/home/engine/project/backend/`:

- `README.md` - Complete setup guide
- `API_EXAMPLES.md` - Curl and Python examples
- `QUICK_START.md` - 5-minute setup
- `PROJECT_SUMMARY.md` - Architecture overview
- `DEPLOYMENT.md` - Production deployment
- `TASK_COMPLETION.md` - Full deliverables

---

## 🧪 Run Tests

```bash
cd /home/engine/project/backend
pytest -v
```

Expected: **24 tests passing** ✅

---

## 🛑 Stop Server

```bash
pkill -f uvicorn
```

---

## 🔄 Restart Server

```bash
cd /home/engine/project/backend
./run.sh
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✨ What's Working

✅ All 15 API endpoints functional
✅ 50 skills loaded
✅ 40 courses loaded  
✅ 15 role clusters loaded
✅ Psychometric profiling
✅ Career matching algorithm
✅ Roadmap generation
✅ Multi-tenant architecture
✅ All tests passing
✅ Interactive documentation
✅ Visual preview page

---

## 🎓 Phase 1 Complete

The GetLanded Career Intelligence Backend is fully operational and ready for:
- Frontend integration
- Pilot deployment
- Further development

**Status**: Production Ready 🚀
