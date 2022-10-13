from urllib import response
#from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from flask_restful import Resource, Request


from models import Highscore



class Scores(Resource):
    # returnerar alla listor i json (listtitle, id)
    def get(self, request):
        scores = list(request.db.database["highscores"].find(limit=100))
        return scores

    def post(self):
        args = list_parser.parse_args()
        db.session.add(Shoppinglist(listTitle=args["newListTitle"]))
        db.session.commit()
        return listTitleInJson() 
    

@router.post("/", response_description = "Add new highscore", status_code=status.HTTP_201_CREATED, response_model=Highscore)
def add_highscore(request: Request, newHighScore: Highscore = Body(...)):
    newHighscore = jsonable_encoder(newHighScore)
    new_highscore= request.app.database["highscores"].insert_one(newHighscore)
    added_highscore = request.app.database["highscores"].find_one(
        {"_id":new_highscore.inserted_id}
    )
    return added_highscore

@router.get("/highscore", response_description="Get the highest 10",)
def get_top_ten(request:Request):
    easy = list(request.app.database["highscores"].find({"difficulty":"easy"}).limit(10).sort("score",-1))
    medium = list(request.app.database["highscores"].find({"difficulty":"medium"}).limit(10).sort("score",-1))
    hard = list(request.app.database["highscores"].find({"difficulty":"hard"}).limit(10).sort("score",-1))
    respons = {
        "easy":easy,
        "medium":medium,
        "hard":hard
    }
    return respons



@router.get("/", response_description="List all Highscores", response_model=List[Highscore])
def list_all_highscores(request:Request):
    highscores = list(request.app.database["highscores"].find(limit=100))
    return highscores

@router.delete("/{id}", response_description="Delete a highscore")
def delete_highsore(id: str, request:Request, response:Response):
    delete_result = request.app.database["highscores"].delete_one({"_id":id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(staus_code=status.HRRP_404_NOT_FOUND, detail=f"Highscore with {id} not found")

@router.delete("/all", response_description="Delete all Highscores")
def delete_all_highscores(request:Request, respons: HighscoreDeleteAll = Body(...)):
    if respons.confirm:
        delete_respons = request.app.database["highscores"].delete_many({"score":{"$gt":0}})
        return f"{delete_respons.deleted_count} documents deletet."
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You must confirm delete.")



