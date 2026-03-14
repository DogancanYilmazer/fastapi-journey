### Why did you choose each Pydantic field type?
id: int – IDs must be numeric value.
name: str – Names are text values.
age: int – Age is a numeric value.
disease: str – Disease name is text.
date: str – Stored as text in DD-MM-YYYY format.
time: str – Stored as text in HH:MM AM/PM format.
Field(gt, ge, lt) – Used to add validation rules like limits for age and length for text fields.

### What does each validation rule protect against?
ge=1 for id - Prevents IDs from being zero or negative.

gt=0, lt=100 for age - Ensures age is a positive and real human age.

min_length=3, max_length=50 for name and disease name - Prevents empty names and extremely long strings that could cause database or UI issues.

Model_validator for appointments - This validation checks the format of the date and time fields.

### Which endpoint uses async in a meaningful way, and why?
GET /appointments/{appointment_id} uses async in a meaningful way because it includes `await asyncio.sleep(1)` to simulate wait.
During this wait, the event loop can process other requests. Endpoint behaves without blocking.
