from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Media, MediaType

router = APIRouter()


class MediaCreate(BaseModel):
    name: str
    genre: str
    actor: str | None = None
    character: str | None = None
    media_type: MediaType
    seasons: int | None = None
    episodes: int | None = None
    release_date: date


@router.get("/medias/")
async def get_medias(db: Session = Depends(get_db)):
    medias = db.query(Media).all()
    if not medias:
        raise HTTPException(status_code=404, detail="No media found")
    return {"medias": medias}


@router.get("/media/{media_id}")
async def get_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(
            status_code=404, detail=f"No media with id {media_id} found"
        )
    return {"media": media}


@router.post("/media/")
async def add_media(media: MediaCreate, db: Session = Depends(get_db)):
    new_media = Media(
        name=media.name,
        genre=media.genre,
        actor=media.actor,
        character=media.character,
        media_type=media.media_type,
        seasons=media.seasons,
        episodes=media.episodes,
        release_date=media.release_date,
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return {"message": "Media created successfully", "media_id": new_media.id}


@router.put("/media/{media_id}")
async def update_media(
    media_id: int, media: MediaCreate, db: Session = Depends(get_db)
):
    old_media = db.query(Media).filter(Media.id == media_id).first()
    if not old_media:
        raise HTTPException(
            status_code=404, detail=f"No media with id {media_id} found"
        )

    old_media.name = media.name if media.name is not None else old_media.name
    old_media.genre = media.genre if media.genre is not None else old_media.genre
    old_media.actor = media.actor if media.actor is not None else old_media.actor
    old_media.character = (
        media.character if media.character is not None else old_media.character
    )
    old_media.media_type = (
        media.media_type if media.media_type is not None else old_media.media_type
    )
    old_media.seasons = (
        media.seasons if media.seasons is not None else old_media.seasons
    )
    old_media.episodes = (
        media.episodes if media.episodes is not None else old_media.episodes
    )
    old_media.release_date = (
        media.release_date if media.release_date is not None else old_media.release_date
    )

    db.commit()
    db.refresh(old_media)
    return {"message": "Media updated successfully"}


@router.delete("/media/{media_id}")
async def delete_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(
            status_code=404, detail=f"No media with id {media_id} found"
        )
    db.delete(media)
    db.commit()
    return {"message": "Media deleted successfully"}
