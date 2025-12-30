from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .routers import (
    students,
    psychometrics,
    career_matches,
    roadmaps,
    tenants,
    reference_data
)
import os

app = FastAPI(
    title="GetLanded Career Intelligence API",
    description="Backend service for student career guidance and roadmap generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tenants.router)
app.include_router(students.router)
app.include_router(psychometrics.router)
app.include_router(career_matches.router)
app.include_router(roadmaps.router)
app.include_router(reference_data.router)

@app.on_event("startup")
def startup_event():
    """Create database tables on startup if they don't exist."""
    from .database.config import engine, Base
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "GetLanded Career Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
        "preview": "/preview"
    }

@app.get("/preview", response_class=HTMLResponse)
def preview():
    """Serve preview page."""
    preview_file = os.path.join(os.path.dirname(__file__), "..", "preview.html")
    try:
        with open(preview_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Preview page not found</h1>"
