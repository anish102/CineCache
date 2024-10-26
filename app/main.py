from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import medias, user_media, users

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(medias.router)
app.include_router(user_media.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Cinecache!"}
