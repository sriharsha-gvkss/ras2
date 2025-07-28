#!/usr/bin/env python3
"""
Database Fix Script
Recreates all database tables with the updated schema.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to Python path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import DATABASE_URL, Base
from app.models import Timesheet, Leave, Email, Task, Job

def reset_database():
    """Drop all tables and recreate them with the new schema"""
    print("🔄 Resetting database with updated schema...")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Drop all tables
        print("📋 Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped successfully")
        
        # Create all tables with new schema
        print("🏗️ Creating tables with new schema...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
        
        # Create session to add some sample data
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Add sample data for testing
            print("📊 Adding sample data...")
            
            # Sample timesheet
            sample_timesheet = Timesheet(
                user_id="user123",
                email="user@example.com",
                date="2024-01-15",
                hours="8",
                description="Development work on AI Assistant",
                submitted=False
            )
            db.add(sample_timesheet)
            
            # Sample leave
            sample_leave = Leave(
                user_id="user123",
                email="user@example.com",
                date="2024-01-20",
                leave_type="Sick Leave",
                reason="Medical appointment",
                status="Pending"
            )
            db.add(sample_leave)
            
            # Sample email
            sample_email = Email(
                user_id="user123",
                email="user@example.com",
                subject="Welcome to AI Assistant",
                message="Thank you for using our AI Assistant platform!",
                type="general",
                status="Unread"
            )
            db.add(sample_email)
            
            # Sample task
            sample_task = Task(
                user_id="user123",
                email="user@example.com",
                title="Complete project documentation",
                description="Write comprehensive documentation for the AI Assistant project",
                priority="High",
                status="Pending"
            )
            db.add(sample_task)
            
            db.commit()
            print("✅ Sample data added successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not add sample data: {e}")
            db.rollback()
        finally:
            db.close()
            
        print("🎉 Database reset completed successfully!")
        print("\n📋 Updated Schema Summary:")
        print("- Timesheets: user_id, email, date, hours, description, submitted, approved_by")
        print("- Leaves: user_id, email, date, leave_type, reason, status, approved_by, approval_comment")
        print("- Emails: user_id, email, subject, message, type, status")
        print("- Tasks: user_id, email, title, description, priority, status")
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database() 