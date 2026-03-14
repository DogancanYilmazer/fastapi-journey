from fastapi import FastAPI
from models import Patients, Appointments # Importing the Pydantic models

app = FastAPI()

patients = [
    {"id": 1, "name": "Evelyn Foster", "age": 30, "disease": "Explosive Diarrhea"},
    {"id": 2, "name": "Jack Davis", "age": 25, "disease": "Zombie Virus"},
    {"id": 3, "name": "Paul Reyes", "age": 40, "disease": "Abdalrahman Syndrome"}
]

appointments = [
    {"id": 1, "name": "Evelyn Foster", "date": "2026-03-01", "time": "10:00 AM"},
    {"id": 2, "name": "Jack Davis", "date": "2026-03-02", "time": "11:00 AM"},
    {"id": 3, "name": "Paul Reyes", "date": "2026-03-03", "time": "12:00 PM"}
]

@app.get("/patients/{patient_id}", response_model=Patients)
def get_patient(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    return {"message": "Patient not found"}

@app.get("/appointments/{appointment_id}", response_model=Appointments)
def get_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return {"message": "Appointment not found"}