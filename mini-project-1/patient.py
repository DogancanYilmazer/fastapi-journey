from fastapi import APIRouter, HTTPException, Request
from models import PatientPublic, PatientCreate, Appointments
from database import managed_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

patient_router = APIRouter()


@patient_router.get("/patients/")
async def get_all_patients():
    with managed_db() as db:
        return {"patients": db.get_all()}


@patient_router.get("/patients/{patient_id}", response_model=PatientPublic)
async def get_patient(patient_id: int):
    with managed_db() as db:
        patient = db.get(patient_id)
        if patient:
            return patient
        raise HTTPException(status_code=404, detail="Patient not found")

@patient_router.get("/appointments/")
async def get_all_appointments():
    with managed_db() as db:
        return {"appointments": db.get_all_appointments()}

@patient_router.get("/appointments/{appointment_id}", response_model=Appointments)
async def get_appointment(appointment_id: int):
    with managed_db() as db:
        appointment = db.get_appointment(appointment_id)
        if appointment:
            return appointment
        raise HTTPException(status_code=404, detail="Appointment not found")

@patient_router.post("/appointments/")
async def add_appointment(appointment: Appointments):
    with managed_db() as db:
        new_id = db.create_appointment(appointment)
        new_appointment = db.get_appointment(new_id)
        return {
            "message": "Appointment added successfully",
            "details": new_appointment
        }

@patient_router.post("/patients/")
async def add_patient(patient: PatientCreate):
    with managed_db() as db:
        new_id = db.create(patient)
        new_patient = db.get(new_id)
        return {
            "message": "Patient added successfully",
            "details": new_patient
        }

@patient_router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, patient: PatientCreate):
    with managed_db() as db:
        updated = db.update(patient_id, patient)
        if updated:
            return {"message": "Patient updated successfully", "details": updated}
        raise HTTPException(status_code=404, detail="Patient not found")

@patient_router.put("/appointments/{appointment_id}")
async def update_appointment(appointment_id: int, appointment: Appointments):
    with managed_db() as db:
        updated = db.update_appointment(appointment_id, appointment)
        if updated:
            return {"message": "Appointment updated successfully", "details": updated}
        raise HTTPException(status_code=404, detail="Appointment not found")

@patient_router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    with managed_db() as db:
        existing = db.get(patient_id)
        if existing:
            db.delete(patient_id)
            return {"message": "Patient deleted successfully", "details": existing}
        raise HTTPException(status_code=404, detail="Patient not found")

@patient_router.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int):
    with managed_db() as db:
        existing = db.get_appointment(appointment_id)
        if existing:
            db.delete_appointment(appointment_id)
            return {"message": "Appointment deleted successfully", "details": existing}
        raise HTTPException(status_code=404, detail="Appointment not found")



@patient_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    with managed_db() as db:
        items = db.get_all()
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={"items": items},
        )


@patient_router.get("/home/{id}", response_class=HTMLResponse)
async def get_item_page(request: Request, id: int):
    with managed_db() as db:
        item = db.get(id)
        if item:
            return templates.TemplateResponse(
                request=request,
                name="patient.html",
                context={"item": item},
            )
        raise HTTPException(status_code=404, detail="Item not found")

