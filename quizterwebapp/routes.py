from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Highscore, HighscoreUpdate

router = APIRouter()

@router.post("/", response_description = "Add new highscore", status_code=status.HTTP_201_CREATED, response_model=Highscore)
def add_highscore(request: Request, newHighScore: Highscore = Body(...)):
    newHighscore = jsonable_encoder(newHighScore)
    new_highscore= request.app.database["highscores"].insert_one(newHighscore)
    added_highscore = request.app.database["highscores"].find_one(
        {"_id":new_highscore.inserted_id}
    )
    return added_highscore

@router.get("/", response_description="List all Highscores", response_model=List[Highscore])
def list_all_highscores(request:Request):
    highscores = list(request.app.database["highscores"].find(limit=100))
    return highscores
