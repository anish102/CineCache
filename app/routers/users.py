from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import (
    Token,
    create_access_token,
    get_admin_user,
    get_current_user,
    get_password_hash,
    verify_password,
)
from app.database import get_db
from app.models import Role, RoleEnum, User

router = APIRouter()


class UserBase(BaseModel):
    name: str
    email: str
    username: str


class UserCreate(UserBase):
    password: str


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/users/", response_model=List[UserBase], dependencies=[Depends(get_current_user)]
)
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.get(
    "/user/{user_id}", response_model=UserBase, dependencies=[Depends(get_current_user)]
)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    return user


@router.post("/user/", dependencies=[Depends(get_admin_user)])
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    role_obj = db.query(Role).filter(Role.name == RoleEnum.user).first()
    if not role_obj:
        raise HTTPException(status_code=400, detail="Role does not exist")

    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    new_user.role.append(role_obj)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@router.put("/user/{user_id}", dependencies=[Depends(get_current_user)])
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    old_user = db.query(User).filter(User.id == user_id).first()
    if not old_user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    old_user.name = user.name
    old_user.email = user.email
    old_user.username = user.username
    db.commit()
    db.refresh(old_user)
    return {"message": "User updated successfully"}


@router.delete("/user/{user_id}", dependencies=[Depends(get_admin_user)])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.post("/setup-first-user")
async def setup_first_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_users = db.query(User).count()
    if existing_users > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Initial setup already completed",
        )
    hashed_password = get_password_hash(user.password)
    admin_role = db.query(Role).filter(Role.name == RoleEnum.admin).first()
    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=admin_role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "First user created successfully", "username": new_user.username}
