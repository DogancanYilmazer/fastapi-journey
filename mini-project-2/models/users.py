from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field

from models.events import Event


class User(Document):
	email: EmailStr
	password: str
	events: Optional[List[Link[Event]]] = Field(default=None)

	class Settings:
		name = "users"


class UserSignUp(BaseModel):
	email: EmailStr
	password: str


class UserSignIn(BaseModel):
	email: EmailStr
	password: str

