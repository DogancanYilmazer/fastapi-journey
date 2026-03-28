### 1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?

An ODM (Object Document Mapper) is a layer that acts as a bridge between Python code and document-based databases like MongoDB. It allows developers to interact with the database using Python objects and classes instead of writing raw queries.

With Beanie, you work with models like Event and User instead of writing raw MongoDB queries.

With Beanie:
event = Event(title="Workshop", description="FastAPI basics")
await event.insert()

Without ODM (raw MongoDB):
await db.events.insert_one({"title": "Workshop", "description": "FastAPI basics"})

### 2. What is the role of the `Database` class — why wrap Beanie methods inside it instead of calling them directly in routes?

The Database class is a service layer that keeps all data-access logic in one place.
This keeps routes focused on request/response handling, avoids repeated query code, and makes testing easier.
Example: instead of writing "await Event.find_one(Event.id == event_id)" in many routes, routes call "await db.get_event(event_id)".


### 3. What happens if `initialize_database()` is not called on startup? What would break and why?

If initialize_database() is not called on startup, Beanie is never initialized with the MongoDB connection and document models.
The app may still start, but database-dependent endpoints (signup/signin/event CRUD) will fail at runtime.

### 4. What is the difference between the `Event` document and the `EventUpdate` model, and why are they two separate classes?

Event is the main Beanie Document model stored in MongoDB. It represents a full event record.

EventUpdate is a request model for update operations. Its fields are optional, so you can change only the fields sent by the client.

Event enforces the structure of saved data.
EventUpdate supports partial updates without forcing all fields every time.