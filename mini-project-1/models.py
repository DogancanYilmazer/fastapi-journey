from pydantic import BaseModel, Field, model_validator

class PatientPublic(BaseModel):
    id: int = Field(ge=1)  # ge means the value must be greater than or equal to 1.
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(gt=0, lt=100)  # Mans the value must be less than 100.

class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0, lt=100)  # gt means greater than 0, and lt means less than 100.
    disease: str = Field(min_length=3, max_length=50)

class Appointments(BaseModel):
    id: int = Field(ge=1)  # Means the value must be greater than or equal to 1.
    name: str = Field(min_length=3, max_length=50)
    date: str
    time: str

    @model_validator(mode="after")
    def validate_date_time(self):
        date = self.date
        time = self.time
        # Basic validation for date and time format (DD-MM-YYYY and HH:MM or HH:MM AM/PM)
        if not date or not time:
            raise ValueError("Date and time are required.")
        if len(date) != 10 or date[2] != '-' or date[5] != '-':
            raise ValueError("Date must be in DD-MM-YYYY format.")
        valid_time = (len(time) == 5 and time[2] == ':') or (len(time) == 8 and time[2] == ':' and time[5] == ' ')
        if not valid_time:
            raise ValueError("Time must be in HH:MM or HH:MM AM/PM format.")
        return self
    
