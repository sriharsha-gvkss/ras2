from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use PostgreSQL with dialogiq_db database
# The DATABASE_URL will be loaded from .env file or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:gvkss@123@localhost:5432/dialogiq_db")

# Create engine with appropriate configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL configuration
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Import models to register them with Base
from app.models.leaves import Leave
from app.models.emails import Email
from app.models.tasks import Task
from app.models.jobs import Job

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
