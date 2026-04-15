from fastapi import FastAPI

from database.connection import initialize_database
from routes.events import router as event_router
from routes.users import router as user_router


app = FastAPI(title="Event Planner API")


@app.on_event("startup")
async def startup_event() -> None:
	await initialize_database()


@app.get("/")
async def root() -> dict:
	return {"message": "Event Planner API is running"}


app.include_router(event_router)
app.include_router(user_router)

