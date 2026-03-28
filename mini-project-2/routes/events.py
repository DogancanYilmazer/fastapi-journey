from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from database.connection import Database
from models.events import Event, EventCreate, EventResponse, EventUpdate


router = APIRouter(prefix="/event", tags=["Events"])
event_database = Database(Event)


def to_event_response(event: Event) -> EventResponse:
	return EventResponse(title=event.title, description=event.description)


@router.get("/", response_model=list[EventResponse])
async def get_events() -> list[EventResponse]:
	events = await event_database.get_all()
	return [to_event_response(event) for event in events]


@router.get("/{id}", response_model=EventResponse)
async def get_event(id: PydanticObjectId) -> EventResponse:
	event = await event_database.get(id)
	if event is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Event not found",
		)
	return to_event_response(event)


@router.post("/new", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate) -> EventResponse:
	new_event = Event(title=event.title, description=event.description)
	saved_event = await event_database.save(new_event)
	return to_event_response(saved_event)


@router.put("/{id}", response_model=EventResponse)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> EventResponse:
	updated_event = await event_database.update(id, body)
	if updated_event is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Event not found",
		)
	return to_event_response(updated_event)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: PydanticObjectId) -> None:
	deleted = await event_database.delete(id)
	if not deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Event not found",
		)

