from urllib import response
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Highscore, HighscoreUpdate, HighscoreDeleteAll, HighscoreHighest

router = APIRouter()

@router.post("/", response_description = "Add new highscore", status_code=status.HTTP_201_CREATED, response_model=Highscore)
def add_highscore(request: Request, newHighScore: Highscore = Body(...)):
    newHighscore = jsonable_encoder(newHighScore)
    new_highscore= request.app.database["highscores"].insert_one(newHighscore)
    added_highscore = request.app.database["highscores"].find_one(
        {"_id":new_highscore.inserted_id}
    )
    return added_highscore

@router.post("/highscore", response_description="Get the highest 10", response_model= HighscoreHighest)
def get_top_ten(request:Request, respons: HighscoreHighest=Body(...)):
    difficulty = jsonable_encoder(respons)
    print(difficulty)
    # highscores = request.app.database["highscores"].find({"difficulty":difficulty}).sort({"score":-1})

    return "highscores"



@router.get("/", response_description="List all Highscores", response_model=List[Highscore])
def list_all_highscores(request:Request):
    highscores = list(request.app.database["highscores"].find(limit=100))
    return highscores

@router.delete("/{id}",response_description="Delete a highscore", response_model=List[Highscore])
def delete_highsore(request:Request):
    delete_result = request.app.database["highscores"].delete_one({"_id":id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(staus_code=status.HRRP_404_NOT_FOUND, detail=f"Highscore with {id} not found")

@router.delete("/all", response_description="Delete all Highscores", response_model=Highscore)
def delete_all_highscores(request:Request, respons: HighscoreDeleteAll = Body(...)):
    if respons.confirm:
        delete_respons = request.app.database["highscores"].delete_many({{score:{"$gt":0}}})
        return f"{delete_respons.deleted_count} documents deletet."
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You must confirm delete.")



