from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field


class ActivityCategory(str, Enum):
    sport = "sport"
    board_games = "board_games"
    walk = "walk"
    club = "club"
    other = "other"


class ActivityStatus(str, Enum):
    open = "OPEN"
    full = "FULL"
    cancelled = "CANCELLED"
    completed = "COMPLETED"


class ActivityCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    category: ActivityCategory
    city: str = Field(min_length=2, max_length=100)
    max_participants: int = Field(ge=2, le=100)


class Activity(ActivityCreate):
    id: int
    status: ActivityStatus = ActivityStatus.open


app = FastAPI(
    title="ActivityHub API",
    description="API для поиска людей для совместных активностей",
    version="0.1.0"
)


activities: list[Activity] = [
    Activity(
        id=1,
        title="Игра в теннис",
        description="Ищем двух человек для парной игры",
        category=ActivityCategory.sport,
        city="Калининград",
        max_participants=4,
        status=ActivityStatus.open
    ),
    Activity(
        id=2,
        title="Настольные игры",
        description="Собираемся поиграть в Манчкин и Имаджинариум",
        category=ActivityCategory.board_games,
        city="Зеленоградск",
        max_participants=6,
        status=ActivityStatus.open
    )
]


@app.get("/")
def root():
    return {
        "project": "ActivityHub",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities", status_code=201)
def create_activity(activity_data: ActivityCreate):
    new_activity = Activity(
        id=len(activities) + 1,
        status=ActivityStatus.open,
        **activity_data.model_dump()
    )

    activities.append(new_activity)

    return new_activity