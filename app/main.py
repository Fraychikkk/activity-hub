from fastapi import FastAPI

app = FastAPI(
    title="ActivityHub API",
    description="API для поиска людей для совместных активностей",
    version="0.1.0"
)


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