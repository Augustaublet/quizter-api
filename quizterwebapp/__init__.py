import imp
from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values
from pymongo import MongoClient
from flask_restful import Api

config = dotenv_values(".env")


client = MongoClient(config["ATLAS_URI"])
db = client[config["DB_NAME"]]


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

    return app


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