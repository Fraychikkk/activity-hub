from enum import Enum
from fastapi import FastAPI, HTTPException
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

next_activity_id = 1


def get_next_activity_id():
    global next_activity_id

    activity_id = next_activity_id
    next_activity_id += 1

    return activity_id

activities: list[Activity] = [
    Activity(
        id=get_next_activity_id(),
        title="Игра в теннис",
        description="Ищем двух человек для парной игры",
        category=ActivityCategory.sport,
        city="Калининград",
        max_participants=4,
        status=ActivityStatus.open
    ),
    Activity(
        id=get_next_activity_id(),
        title="Настольные игры",
        description="Собираемся поиграть в настольные игры",
        category=ActivityCategory.board_games,
        city="Зеленоградск",
        max_participants=6,
        status=ActivityStatus.open
    )
]


@app.get("/")
def root():
    return {
        "message": "Hello from ActivityHub API",
        "project": "ActivityHub",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@app.get("/info")
def app_info():
    return {
        "app": "activity-hub",
        "version": "0.1.0",
        "port": 8000
    }

@app.get("/activities")
def get_activities(
    city: str | None = None,
    category: ActivityCategory | None = None,
    status: ActivityStatus | None = None
):
    result = activities

    if city is not None:
        result = [
            activity for activity in result
            if activity.city.lower() == city.lower()
        ]

    if category is not None:
        result = [
            activity for activity in result
            if activity.category == category
        ]

    if status is not None:
        result = [
            activity for activity in result
            if activity.status == status
        ]

    return result

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int):
    for activity in activities:
        if activity.id == activity_id:
            return activity

    raise HTTPException(
        status_code=404,
        detail="Activity not found"
    )

@app.post("/activities", status_code=201)
def create_activity(activity_data: ActivityCreate):
    new_activity = Activity(
    id=get_next_activity_id(),
    status=ActivityStatus.open,
    **activity_data.model_dump()
    )

    activities.append(new_activity)

    return new_activity