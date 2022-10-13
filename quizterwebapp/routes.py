from urllib import response
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from . import db
from quizterwebapp import db

from models import Score

DATABASE_NAME = "Highscore"

router = APIRouter()

@router.post("/", response_description = "Add new Score", status_code=status.HTTP_201_CREATED, response_model=Score)
def add_Score(request: Request, response: Score = Body(...)):
    newScore = jsonable_encoder(response)
    new_score= request.db.database[DATABASE_NAME].insert_one(newScore)
    added_score = request.db.database[DATABASE_NAME].find_one(
        {"_id":new_score.inserted_id}
    )
    return added_score

@router.get("/highscore", response_description="Get the highest 10",)
def get_top_ten(request:Request):
    easy = list(request.db.database[DATABASE_NAME].find({"difficulty":"easy"}).limit(10).sort("score",-1))
    medium = list(request.db.database[DATABASE_NAME].find({"difficulty":"medium"}).limit(10).sort("score",-1))
    hard = list(request.db.database[DATABASE_NAME].find({"difficulty":"hard"}).limit(10).sort("score",-1))
    respons = {
        "easy":easy,
        "medium":medium,
        "hard":hard
    }
    return respons

@router.get("/", response_description="List all Scores", response_model=List[Score])
def list_all_Scores(request:Request):
    scores = list(request.db.database[DATABASE_NAME].find(limit=100))
    return scores
