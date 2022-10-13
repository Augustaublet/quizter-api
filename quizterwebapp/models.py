import uuid

from pydantic import BaseModel, Field

class Highscore(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    playerName: str = Field(...)
    difficulty: str = Field(...)
    categories: list[str] = []
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
                "categories": ["Sports", "History"]
            }
        }