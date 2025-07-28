from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.emails import EmailCreate, EmailOut
from app.models.emails import Email
from app.database import get_db
from typing import List

router = APIRouter(prefix="/emails", tags=["Emails"])

@router.post("/", response_model=EmailOut)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    print("✅ Email API called from Rasa")
    try:
        db_email = Email(**email.dict())
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        return EmailOut.from_orm(db_email)
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create email: {str(e)}")

@router.get("/", response_model=List[EmailOut])
def list_emails(db: Session = Depends(get_db)):
    try:
        emails = db.query(Email).all()
        return [EmailOut.from_orm(email) for email in emails]
    except Exception as e:
        print(f"❌ Error listing emails: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list emails: {str(e)}")

@router.get("/remind-pending-timesheets", response_model=List[EmailOut])
def remind_pending_timesheets_emails(db: Session = Depends(get_db)):
    try:
        emails = db.query(Email).filter(Email.type == "reminder", Email.status == "Unread").all()
        return [EmailOut.from_orm(email) for email in emails]
    except Exception as e:
        print(f"❌ Error listing reminder emails: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list reminder emails: {str(e)}")

@router.get("/submit-pending-timesheets", response_model=List[EmailOut])
def submit_pending_timesheets_emails(db: Session = Depends(get_db)):
    try:
        emails = db.query(Email).filter(Email.type == "submit", Email.status == "Unread").all()
        return [EmailOut.from_orm(email) for email in emails]
    except Exception as e:
        print(f"❌ Error listing submit emails: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list submit emails: {str(e)}")

@router.post("/draft", response_model=EmailOut)
def create_draft_email(email: EmailCreate, db: Session = Depends(get_db)):
    try:
        data = email.dict()
        data["status"] = "Draft"
        db_email = Email(**data)
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        return EmailOut.from_orm(db_email)
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating draft email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create draft email: {str(e)}")

@router.get("/drafts", response_model=List[EmailOut])
def list_draft_emails(db: Session = Depends(get_db)):
    try:
        emails = db.query(Email).filter(Email.status == "Draft").all()
        return [EmailOut.from_orm(email) for email in emails]
    except Exception as e:
        print(f"❌ Error listing draft emails: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list draft emails: {str(e)}")

@router.get("/{email_id}/context", response_model=EmailOut)
def provide_email_context(email_id: int, db: Session = Depends(get_db)):
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        # Here you could add more context if needed
        return EmailOut.from_orm(email)
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting email context: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get email context: {str(e)}") 