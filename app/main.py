from app.database import engine
from app.models import Base
from app.routers import users
from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Cinecache!"}
