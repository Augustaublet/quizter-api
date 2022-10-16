from urllib import response
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from deta import Deta
from dotenv import dotenv_values

from models import Score

router = APIRouter()


config = dotenv_values(".env")

deta = Deta(config["DETA_KEY"])
db = deta.Base("test_db1")


@router.post("/", response_description = "Add new highscore", status_code=status.HTTP_201_CREATED, response_model=Score)
def add_highscore(score: Score = Body(...)):
    added_score = db.put(jsonable_encoder(score))
    return added_score

@router.get("/highscore", response_description="Get the highest 10",)
def get_top_ten():
    data = db.fetch()
    easy = []
    medium = []
    hard = []
    

    # easy = Implement sorting of fetch...
    # medium = Implement sorting of fetch...
    # hard = Implement sorting of fetch...
    respons = {
        "easy":easy,
        "medium":medium,
        "hard":hard
    }
    return respons



@router.get("/", response_description="List all Highscores", response_model=List[Score])
def list_all_highscores():
    scores = db.fetch()
    return scores.items

# @router.delete("/{id}", response_description="Delete a highscore")
# def delete_highsore(id: str, request:Request, response:Response):
#     delete_result = request.app.database["highscores"].delete_one({"_id":id})

#     if delete_result.deleted_count == 1:
#         response.status_code = status.HTTP_204_NO_CONTENT
#         return response
    
#     raise HTTPException(staus_code=status.HRRP_404_NOT_FOUND, detail=f"Score with {id} not found")

# @router.delete("/all", response_description="Delete all Highscores")
# def delete_all_highscores(request:Request, respons: HighscoreDeleteAll = Body(...)):
#     if respons.confirm:
#         delete_respons = request.app.database["highscores"].delete_many({"score":{"$gt":0}})
#         return f"{delete_respons.deleted_count} documents deletet."
    
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You must confirm delete.")



