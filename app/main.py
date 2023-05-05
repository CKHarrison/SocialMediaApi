from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Only need this command for sqlAlchemy to create the tables upon first save
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# use this to manage cors policy
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "What is love?"}
