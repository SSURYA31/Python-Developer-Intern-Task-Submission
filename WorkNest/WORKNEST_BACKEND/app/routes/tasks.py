


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..database import SessionLocal
from ..models import Task

SECRET_KEY = "secret"
ALGORITHM = "HS256"

router = APIRouter()
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["user_id"]


# CREATE TASK
@router.post("/tasks")
def create_task(data: dict, db: Session = Depends(get_db), user_id=Depends(get_user)):
    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        comment=data.get("comment"),
        time_period=data.get("time_period"),
        status="Pending",
        completed=False,
        owner_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


#  GET TASKS
@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db), user_id=Depends(get_user)):
    return db.query(Task).filter(Task.owner_id == user_id).all()


#  UPDATE TASK (MARK COMPLETE)
@router.put("/tasks/{task_id}/complete")
def mark_complete(task_id: int, db: Session = Depends(get_db), user_id=Depends(get_user)):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.completed:
        return {"message": "Task already completed"}

    task.completed = True
    db.commit()
    db.refresh(task)

    return {"message": "Task marked as completed", "task": task}


#  DELETE TASK
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user_id=Depends(get_user)):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

#  GET SINGLE TASK
@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), user_id=Depends(get_user)):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# UPDATE TASK (EDIT DETAILS)
@router.put("/tasks/{task_id}")
def update_task(task_id: int, data: dict, db: Session = Depends(get_db), user_id=Depends(get_user)):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = data.get("title")
    task.description = data.get("description")
    task.comment = data.get("comment")
    task.time_period = data.get("time_period")

    db.commit()
    db.refresh(task)

    return task