from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import timesheet, leaves, emails, tasks, jobs, auth
from app.database import Base, engine

# Import all models to register them with Base
from app.models import Timesheet, Leave, Email, Task, Job

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Assistant Backend", version="1.0.0")

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(timesheet.router)
app.include_router(leaves.router)
app.include_router(emails.router)
app.include_router(tasks.router)
app.include_router(jobs.router)

@app.get("/")
async def root():
    return {"message": "AI Assistant Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}