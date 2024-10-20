from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

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


@router.put("/user/{user_id}")
async def read_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    old_user = db.query(User).filter(User.id == user_id).first()
    if not old_user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    old_user.name = user.name if user.name else None
    old_user.email = user.email if user.email else None
    old_user.username = user.username if user.username else None
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully"}


@router.delete("/user/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
