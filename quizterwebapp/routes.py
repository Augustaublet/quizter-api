from urllib import response
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Score, ScoreDeleteAll

DATABASE_NAME = "Highscore"

router = APIRouter()

@router.post("/", response_description = "Add new Score", status_code=status.HTTP_201_CREATED, response_model=Score)
def add_Score(request: Request, response: Score = Body(...)):
    newScore = jsonable_encoder(response)
    new_score= request.app.database[DATABASE_NAME].insert_one(newScore)
    added_score = request.app.database[DATABASE_NAME].find_one(
        {"_id":new_score.inserted_id}
    )
    return added_score

@router.get("/highscore", response_description="Get the highest 10",)
def get_top_ten(request:Request):
    easy = list(request.app.database[DATABASE_NAME].find({"difficulty":"easy"}).limit(10).sort("score",-1))
    medium = list(request.app.database[DATABASE_NAME].find({"difficulty":"medium"}).limit(10).sort("score",-1))
    hard = list(request.app.database[DATABASE_NAME].find({"difficulty":"hard"}).limit(10).sort("score",-1))
    respons = {
        "easy":easy,
        "medium":medium,
        "hard":hard
    }
    return respons

@router.get("/", response_description="List all Scores", response_model=List[Score])
def list_all_Scores(request:Request):
    scores = list(request.app.database[DATABASE_NAME].find(limit=100))
    return scores



@router.delete("/{id}", response_description="Delete a Score")
def delete_Sore(id: str, request:Request, response:Response):
    delete_result = request.app.database[DATABASE_NAME].delete_one({"_id":id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(staus_code=status.HRRP_404_NOT_FOUND, detail=f"Score with {id} not found")

@router.delete("/all", response_description="Delete all Scores")
def delete_all_Scores(request:Request, respons: ScoreDeleteAll = Body(...)):
    if respons.confirm:
        delete_respons = request.app.database[DATABASE_NAME].delete_many({"score":{"$gt":0}})
        return f"{delete_respons.deleted_count} documents deletet."
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You must confirm delete.")



