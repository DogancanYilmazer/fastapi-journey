from typing import Any, Dict, List, Optional, Type, cast

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from models.events import Event
from models.users import User


class Settings(BaseSettings):
	database_url: str = Field(alias="DATABASE_URL")

	model_config = SettingsConfigDict(
		env_file=".env",
		extra="ignore",
		populate_by_name=True,
	)


settings = Settings()  # pyright: ignore[reportCallIssue]


async def initialize_database() -> None:
	if not settings.database_url:
		raise ValueError("DATABASE_URL is not set. Add it to your .env file.")

	client = AsyncIOMotorClient(settings.database_url)
	database = cast(Any, client.get_default_database())
	await init_beanie(
		database=database,
		document_models=[Event, User],
	)


class Database:
	def __init__(self, model: Type[Document]):
		self.model = model

	async def save(self, document: Document) -> Document:
		await document.insert()
		return document

	async def get(self, document_id: Any) -> Optional[Document]:
		return await self.model.get(document_id)

	async def get_all(self) -> List[Document]:
		return await self.model.find_all().to_list()

	async def update(self, document_id: Any, body: Any) -> Optional[Document]:
		document = await self.get(document_id)
		if document is None:
			return None

		if hasattr(body, "model_dump"):
			update_data: Dict[str, Any] = body.model_dump(exclude_unset=True)
		elif isinstance(body, dict):
			update_data = body
		else:
			update_data = {}

		for key, value in update_data.items():
			setattr(document, key, value)

		await document.save()
		return document

	async def delete(self, document_id: Any) -> bool:
		document = await self.get(document_id)
		if document is None:
			return False

		await document.delete()
		return True

