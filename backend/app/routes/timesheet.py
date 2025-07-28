from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.timesheet import TimesheetCreate, TimesheetOut
from app.models.timesheet import Timesheet
from app.database import get_db
from typing import List

router = APIRouter(prefix="/timesheets", tags=["Timesheets"])

@router.post("/", response_model=TimesheetOut)
def create_timesheet(timesheet: TimesheetCreate, db: Session = Depends(get_db)):
    print("✅ Timesheet API called from Rasa")
    try:
        db_ts = Timesheet(**timesheet.dict())
        db.add(db_ts)
        db.commit()
        db.refresh(db_ts)
        return TimesheetOut.from_orm(db_ts)
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating timesheet: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create timesheet: {str(e)}")

@router.get("/", response_model=List[TimesheetOut])
def list_timesheets(db: Session = Depends(get_db)):
    try:
        timesheets = db.query(Timesheet).all()
        return [TimesheetOut.from_orm(ts) for ts in timesheets]
    except Exception as e:
        print(f"❌ Error listing timesheets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list timesheets: {str(e)}")

@router.put("/{timesheet_id}", response_model=TimesheetOut)
def update_timesheet(timesheet_id: int, timesheet: TimesheetCreate, db: Session = Depends(get_db)):
    try:
        db_ts = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
        if not db_ts:
            raise HTTPException(status_code=404, detail="Timesheet not found")
        for key, value in timesheet.dict().items():
            setattr(db_ts, key, value)
        db.commit()
        db.refresh(db_ts)
        return TimesheetOut.from_orm(db_ts)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating timesheet: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update timesheet: {str(e)}")

@router.post("/{timesheet_id}/approve", response_model=TimesheetOut)
def approve_timesheet(timesheet_id: int, approver: str, db: Session = Depends(get_db)):
    try:
        db_ts = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
        if not db_ts:
            raise HTTPException(status_code=404, detail="Timesheet not found")
        db_ts.submitted = True
        db_ts.approved_by = approver
        db.commit()
        db.refresh(db_ts)
        return TimesheetOut.from_orm(db_ts)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error approving timesheet: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to approve timesheet: {str(e)}")

@router.get("/pending", response_model=List[TimesheetOut])
def list_pending_timesheets(db: Session = Depends(get_db)):
    try:
        timesheets = db.query(Timesheet).filter(Timesheet.submitted == False).all()
        return [TimesheetOut.from_orm(ts) for ts in timesheets]
    except Exception as e:
        print(f"❌ Error listing pending timesheets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list pending timesheets: {str(e)}")

@router.post("/send-pending", response_model=List[TimesheetOut])
def send_pending_timesheets(approver: str, db: Session = Depends(get_db)):
    try:
        pending = db.query(Timesheet).filter(Timesheet.submitted == False).all()
        for ts in pending:
            ts.submitted = True
            ts.approved_by = approver
        db.commit()
        return [TimesheetOut.from_orm(ts) for ts in pending]
    except Exception as e:
        db.rollback()
        print(f"❌ Error sending pending timesheets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send pending timesheets: {str(e)}")
