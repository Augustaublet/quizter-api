from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as highscore_router
from flask import Flask

config = dotenv_values(".env")

flask_app = Flask(__name__)

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(highscore_router, tags=["scores"], prefix="/scores")

app.mount("/scores", WSGIMiddleware(flask_app))