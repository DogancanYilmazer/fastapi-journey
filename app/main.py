import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title=os.getenv("APP_NAME", "Simple Polls"))

polls = {}
connections = {}

app.mount("/static", StaticFiles(directory="app/static"), name="static")


class PollCreate(BaseModel):
    question: str
    options: list[str]


class Vote(BaseModel):
    option: str

@app.get("/", include_in_schema=False)
def home():
    return FileResponse("app/static/index.html")


@app.post("/polls", status_code=201)
def create_poll(data: PollCreate):
    options = [x.strip() for x in data.options if x.strip()]
    if len(options) < 2:
        raise HTTPException(status_code=400, detail="At least 2 options required")

    poll_id = str(uuid4())
    polls[poll_id] = {
        "id": poll_id,
        "question": data.question,
        "options": options,
        "votes": {option: 0 for option in options},
    }
    return polls[poll_id]


@app.get("/polls")
def list_polls():
    return list(polls.values())


@app.get("/polls/{poll_id}")
def get_poll(poll_id: str):
    return get_poll_or_404(poll_id)


@app.post("/polls/{poll_id}/vote")
async def vote_rest(poll_id: str, data: Vote):
    poll = get_poll_or_404(poll_id)
    if data.option not in poll["votes"]:
        raise HTTPException(status_code=400, detail="Invalid option")

    poll["votes"][data.option] += 1
    return poll


@app.delete("/polls/{poll_id}", status_code=204)
async def delete_poll(poll_id: str):
    get_poll_or_404(poll_id)
    
    # Notify WebSocket clients that the poll was deleted
    message = {"type": "poll_deleted"}
    for ws in connections.get(poll_id, [])[:]:
        try:
            await ws.send_json(message)
        except Exception:
            if poll_id in connections:
                connections[poll_id].remove(ws)
    
    # Clean up connections for this poll
    if poll_id in connections:
        del connections[poll_id]
    
    del polls[poll_id]

def get_poll_or_404(poll_id: str):
    poll = polls.get(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

