from database import engine
from fastapi import FastAPI
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
