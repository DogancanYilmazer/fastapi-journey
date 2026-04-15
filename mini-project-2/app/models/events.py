from typing import Optional

from beanie import Document
from pydantic import BaseModel


class Event(Document):
	title: str
	description: str

	class Settings:
		name = "events"


class EventCreate(BaseModel):
	title: str
	description: str


class EventResponse(BaseModel):
	title: str
	description: str


class EventUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None

