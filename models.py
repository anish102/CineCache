from enum import Enum as PyEnum

from database import Base
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class WatchStatus(PyEnum):
    watched = "watched"
    to_watch = "to-watch"
    watching = "watching"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    movies = relationship("Movie", back_populates="user")
    series = relationship("Series", back_populates="user")
    anime = relationship("Anime", back_populates="user")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String)
    actor = Column(String)
    release_date = Column(Date)
    status = Column(Enum(WatchStatus))
    rating = Column(Integer)
    added_on = Column(Date, server_default=func.current_date())
    watched_on = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="movies")


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String)
    seasons = Column(Integer)
    episodes = Column(Integer)
    actor = Column(String)
    release_date = Column(Date)
    status = Column(Enum(WatchStatus))
    rating = Column(Integer)
    added_on = Column(Date, server_default=func.current_date())
    watched_on = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="series")


class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String)
    seasons = Column(Integer)
    episodes = Column(Integer)
    character = Column(String)
    release_date = Column(Date)
    status = Column(Enum(WatchStatus))
    rating = Column(Integer)
    added_on = Column(Date, server_default=func.current_date())
    watched_on = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="anime")
