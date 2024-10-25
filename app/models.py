from enum import Enum

from sqlalchemy import Column, Date
from sqlalchemy import Enum as SQLenum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class WatchStatus(Enum):
    watched = "watched"
    to_watch = "to-watch"
    watching = "watching"


class MediaType(Enum):
    movie = "movie"
    series = "series"
    anime = "anime"


class UserMedia(Base):
    __tablename__ = "user_media"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    media_id = Column(Integer, ForeignKey("media.id"))
    status = Column(SQLenum(WatchStatus), nullable=False)
    rating = Column(Integer)
    added_on = Column(Date)
    watched_on = Column(Date, nullable=True)
    user = relationship("User", back_populates="media_associations")
    media = relationship("Media", back_populates="user_associations")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    media_associations = relationship("UserMedia", back_populates="user")


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String)
    media_type = Column(SQLenum(MediaType))
    actor = Column(String, nullable=True)
    character = Column(String, nullable=True)
    seasons = Column(Integer, nullable=True)
    episodes = Column(Integer, nullable=True)
    release_date = Column(Date)
    user_associations = relationship("UserMedia", back_populates="media")
