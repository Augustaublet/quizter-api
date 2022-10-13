import imp
from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values
from pymongo import MongoClient
from flask_restful import Api
import atexit
config = dotenv_values(".env")


client = MongoClient(config["ATLAS_URI"])
db = client[config["DB_NAME"]]

def shutdown_db_client(): # called at the end by atexit to terminate the conection
    db.client.close()


from quizterwebapp import routes
from quizterwebapp import models
# from .routes import GetShoppingLists

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    CORS(app)
    api = Api(app)
    
    create_datebase(app)

    api.add_resource(routes.ShoppingListsResorce, "/shoppinglist/","/shoppinglist/<list_id>")
    api.add_resource(routes.ListItemResorce, "/shoppinglist/items/<list_id>", "/shoppinglist/items/<list_id>/<item_id>" )

    atexit(shutdown_db_client)
    return app


app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    db.client.close()

app.include_router(highscore_router, tags=["scores"], prefix="/scores")