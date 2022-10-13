import imp
from dotenv import dotenv_values
from pymongo import MongoClient
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import atexit
config = dotenv_values(".env")


client = MongoClient(config["ATLAS_URI"])
db = client[config["DB_NAME"]]
print("Connected to the MongoDB database!")

# app.mongodb_client = MongoClient(config["ATLAS_URI"])
# app.database = app.mongodb_client[config["DB_NAME"]]
def shutdown_db_client():
    db.mongodb_client.close()

from quizterwebapp import routes
from quizterwebapp import models   

def create_app():
    app= Flask(__name__)

    
    

    CORS(app)
    api = Api(app)

    

    #app.include_router(highscore_router, tags=["scores"], prefix="/scores")

    api.add_resource(routes.Highscore, "/score")

    atexit(shutdown_db_client)
    return app
    

# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient(config["ATLAS_URI"])
#     app.database = app.mongodb_client[config["DB_NAME"]]
#     print("Connected to the MongoDB database!")

# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()

