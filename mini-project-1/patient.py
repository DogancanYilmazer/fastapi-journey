from fastapi import APIRouter, HTTPException, Request
from models import PatientPublic, PatientCreate, Appointments
import asyncio
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

patient_router = APIRouter()

patients = [
    {"id": 1, "name": "Evelyn Foster", "age": 30, "disease": "Explosive Diarrhea"},
    {"id": 2, "name": "Jack Davis", "age": 25, "disease": "Zombie Virus"},
    {"id": 3, "name": "Paul Reyes", "age": 40, "disease": "Abdalrahman Syndrome"}
]

appointments = [
    {"id": 1, "name": "Evelyn Foster", "date": "01-03-2026", "time": "10:00 AM"},
    {"id": 2, "name": "Jack Davis", "date": "02-03-2026", "time": "11:00 AM"},
    {"id": 3, "name": "Paul Reyes", "date": "03-03-2026", "time": "12:00 PM"}
]


@patient_router.get("/patients/{patient_id}", response_model=PatientPublic)
async def get_patient(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404,
                        detail="Patient not found"
    )

@patient_router.get("/appointments/{appointment_id}", response_model=Appointments)
async def get_appointment(appointment_id: int):
    await asyncio.sleep(1) # import asyncio to use this for simulating delay
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    raise HTTPException(status_code=404,
                        detail="Appointment not found"
    )

@patient_router.post("/patients/")
async def add_patient(patient: PatientCreate):
    patient_id = max(p["id"] for p in patients) + 1 if patients else 1
    new_patient = {
        "id": patient_id,
        "name": patient.name,
        "age": patient.age,
        "disease": patient.disease
    }
    patients.append(new_patient)
    return {
        "message": "Patient added successfully",
        "details": {
            "id": new_patient["id"],
            "name": new_patient["name"],
            "age": new_patient["age"]
        }
    }

@patient_router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, patient: PatientCreate):
    for p in patients:
        if p["id"] == patient_id:
            p["name"] = patient.name
            p["age"] = patient.age
            p["disease"] = patient.disease
            return {"message": "Patient updated successfully", "details": p}
    raise HTTPException(status_code=404,
                        detail="Patient not found"
    )

@patient_router.put("/appointments/{appointment_id}")
async def update_appointment(appointment_id: int, appointment: Appointments):
    for a in appointments:
        if a["id"] == appointment_id:
            a["name"] = appointment.name
            a["date"] = appointment.date
            a["time"] = appointment.time
            return {"message": "Appointment updated successfully", "details": a}
    raise HTTPException(status_code=404,
                        detail="Appointment not found"
    )

@patient_router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    for p in patients:
        if p["id"] == patient_id:
            patients.remove(p)
            return {"message": "Patient deleted successfully", "details": p}
    raise HTTPException(status_code=404,
                        detail="Patient not found"
    )

@patient_router.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int):
    for a in appointments:
        if a["id"] == appointment_id:
            appointments.remove(a)
            return {"message": "Appointment deleted successfully", "details": a}
    raise HTTPException(status_code=404,
                        detail="Appointment not found"
    )



@patient_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": patients
    })


@patient_router.get("/home/{id}", response_class=HTMLResponse)
async def get_item_page(request: Request, id: int):
    for item in patients:
        if item["id"] == id:
            return templates.TemplateResponse("patient.html", {
                "request": request,
                "item": item
            })
    raise HTTPException(status_code=404,
                         detail="Item not found"
    )

