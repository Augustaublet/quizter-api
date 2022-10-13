from lib2to3.pgen2.token import OP
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Score(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    playerName: str = Field(...)
    difficulty: str = Field(...)
    #categories
    score: int = Field(...)
    longestStreak: int = Field(...)
    numberOfQuestions: int = Field(...)
    categories: list[str] = []

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "playerName": "Kalle Anka",
                "difficulty": "medium",
                "score": 12,
                "longestStreak": 4,
                "numberOfQuestions": 15,
                "categories": ["Art & literature", "Sports"]
            }
        }
class ScoreUpdate(BaseModel):
    name: Optional[str]
    difficulty: Optional[str]
    score: Optional[int]
    longestStreak: Optional[int]
    numberOfQuestions: Optional[int]
    categories: Optional[list]

    class Config:
        schema_extra = {
            "example": {
                "playerName": "Kalle Anka",
                "difficulty": "medium",
                "score": 12,
                "longestStreak": 4,
                "numberOfQuestions": 15,
                "categories": ["Art & literature", "Sports"]
            }
        }

class ScoreDeleteAll(BaseModel):
    confirm: bool
    class Config:
        schema_extra = {
            "example": {
                "confirm": True
            }
        }