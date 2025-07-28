from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.leaves import LeaveCreate, LeaveOut, LeaveUpdate
from app.models.leaves import Leave
from app.database import get_db
from typing import List

router = APIRouter(prefix="/leaves", tags=["Leaves"])

@router.post("/", response_model=LeaveOut)
def create_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    print("✅ Leave API called from Rasa")
    try:
        db_leave = Leave(**leave.dict())
        db.add(db_leave)
        db.commit()
        db.refresh(db_leave)
        return LeaveOut.from_orm(db_leave)
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating leave: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create leave: {str(e)}")

@router.get("/", response_model=List[LeaveOut])
def list_leaves(db: Session = Depends(get_db)):
    try:
        leaves = db.query(Leave).all()
        return [LeaveOut.from_orm(leave) for leave in leaves]
    except Exception as e:
        print(f"❌ Error listing leaves: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list leaves: {str(e)}")

@router.put("/{leave_id}", response_model=LeaveOut)
def update_leave(leave_id: int, leave: LeaveUpdate, db: Session = Depends(get_db)):
    try:
        db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
        if not db_leave:
            raise HTTPException(status_code=404, detail="Leave not found")
        
        for key, value in leave.dict(exclude_unset=True).items():
            setattr(db_leave, key, value)
        
        db.commit()
        db.refresh(db_leave)
        return LeaveOut.from_orm(db_leave)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating leave: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update leave: {str(e)}") 