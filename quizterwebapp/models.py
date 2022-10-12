import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Highscore(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    playerName: str = Field(...)
    difficulty: str = Field(...)
    #categories
    score: int = Field(...)
    longestStreak: int = Field(...)
    numberOfQuestions: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "playerName": "Kalle Anka",
                "difficulty": "medium",
                "score": 12,
                "longestStreak": 4,
                "numberOfQuestions": 15,
            }
        }
class HighscoreUpdate(BaseModel):
    name: Optional[str]
    difficulty: Optional[str]
    score: Optional[int]
    longestStreak: Optional[int]
    numberOfQuestions: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "playerName": "Kalle Anka",
                "difficulty": "medium",
                "score": 12,
                "longestStreak": 4,
                "numberOfQuestions": 15,
            }
        }
class HighscoreHighest(BaseModel):
    difficulty: Optional[str]
    
    class Config:
        schema_extra = {
            "example":{
                "difficulty":"medium",
            }
        }

class HighscoreDeleteAll(BaseModel):
    confirm: bool
    class Config:
        schema_extra = {
            "example": {
                "confirm": True
            }
        }