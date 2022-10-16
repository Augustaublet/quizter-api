from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as highscore_router


config = dotenv_values(".env")


app = FastAPI()


app.include_router(highscore_router, tags=["scores"], prefix="/scores")