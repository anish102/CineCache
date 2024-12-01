from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Media, User, UserMedia, WatchStatus

router = APIRouter()


class UserMediaCreate(BaseModel):
    media_id: int
    status: WatchStatus
    rating: int | None = None


class UserMediaUpdate(BaseModel):
    status: WatchStatus | None = None
    rating: int | None = None


@router.post("/user/{user_id}/media/")
async def add_user_media(
    user_id: int, user_media: UserMediaCreate, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    media = db.query(Media).filter(Media.id == user_media.media_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} found")
    if not media:
        raise HTTPException(
            status_code=404, detail=f"No media with id {user_media.media_id} found"
        )

    new_user_media =    (
        user_id=user.id,
        media_id=media.id,
        status=user_media.status,
        rating=user_media.rating,
        added_on=date.today(),
    )
    db.add(new_user_media)
    db.commit()
    db.refresh(new_user_media)
    return {
        "message": "User media created successfully",
        "user_media_id": new_user_media.id,
    }


@router.put("/user/media/{user_media_id}")
async def update_user_media(
    user_media_id: int,
    user_media_update: UserMediaUpdate,
    db: Session = Depends(get_db),
):
    user_media = db.query(UserMedia).filter(UserMedia.id == user_media_id).first()

    if not user_media:
        raise HTTPException(
            status_code=404, detail=f"No user media with id {user_media_id} found"
        )

    if user_media_update.status is not None:
        user_media.status = user_media_update.status
    if user_media_update.rating is not None:
        user_media.rating = user_media_update.rating

    db.commit()
    db.refresh(user_media)
    return {"message": "User media updated successfully"}


@router.delete("/user/media/{user_media_id}")
async def delete_user_media(user_media_id: int, db: Session = Depends(get_db)):
    user_media = db.query(UserMedia).filter(UserMedia.id == user_media_id).first()

    if not user_media:
        raise HTTPException(
            status_code=404, detail=f"No user media with id {user_media_id} found"
        )

    db.delete(user_media)
    db.commit()
    return {"message": "User media deleted successfully"}


@router.get("/user/{user_id}/media/")
async def get_user_media(user_id: int, db: Session = Depends(get_db)):
    user_media_list = db.query(UserMedia).filter(UserMedia.user_id == user_id).all()
    return {"user_media": user_media_list}
