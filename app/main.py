from fastapi import FastAPI
from pydantic import BaseSettings
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Only need this command for sqlAlchemy to create the tables upon first save
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "What is love?"}
