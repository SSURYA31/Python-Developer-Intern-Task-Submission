from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate
from ..auth import hash_password, verify_password, create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    yield db
    db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return {"error": "Invalid login"}

    token = create_token({"user_id": db_user.id})
    return {"access_token": token}