from fastapi import FastAPI
from patient import patient_router
app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to the Clinic API"}

app.include_router(patient_router)