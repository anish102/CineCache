from app.database import get_db
from app.models import User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str
    username: str


@router.get("/users/")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"users": users}


@router.get("/user/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    return {"user": user}


@router.post("/user/")
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}
