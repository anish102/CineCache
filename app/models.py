from enum import Enum as PyEnum

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class WatchStatus(PyEnum):
    watched = "watched"
    to_watch = "to-watch"
    watching = "watching"


class MediaType(PyEnum):
    movie = "movie"
    series = "series"
    anime = "anime"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    media = relationship("Media", back_populates="user")


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String)
    media_type = Column(Enum(MediaType))
    actor = Column(String, nullable=True)
    character = Column(String, nullable=True)
    seasons = Column(Integer, nullable=True)
    episodes = Column(Integer, nullable=True)
    release_date = Column(Date)
    status = Column(Enum(WatchStatus))
    rating = Column(Integer)
    added_on = Column(Date, server_default=func.current_date())
    watched_on = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="media")
