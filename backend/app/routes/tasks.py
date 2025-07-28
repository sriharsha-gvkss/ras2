from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tasks import TaskCreate, TaskOut
from app.models.tasks import Task
from app.database import get_db
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    print("✅ Task API called from Rasa")
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return TaskOut.from_orm(db_task)
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@router.get("/", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()
        return [TaskOut.from_orm(task) for task in tasks]
    except Exception as e:
        print(f"❌ Error listing tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list tasks: {str(e)}") 