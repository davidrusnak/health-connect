from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import httpx

# Define the FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./patients.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Patient model
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for response
class PatientResponse(BaseModel):
    id: int
    data: dict

    class Config:
        orm_mode = True

# Helper function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get a specific patient
@app.get("/patient/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int, db: Session = next(get_db())):
    # Check if the patient exists in the local database
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if patient is None:
        # Fetch patient data from external API
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:32783/fhir/r4/Patient/{patient_id}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Patient not found")
        
        # Store the fetched patient data in the local database
        new_patient = Patient(id=patient_id, data=response.json())
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return PatientResponse(id=new_patient.id, data=new_patient.data)
    
    return PatientResponse(id=patient.id, data=patient.data)

# Endpoint to get all patients
@app.get("/patient", response_model=list[PatientResponse])
async def get_all_patients(db: Session = next(get_db())):
    patients = db.query(Patient).all()
    return [PatientResponse(id=patient.id, data=patient.data) for patient in patients]

# To run the app, use the command: uvicorn filename:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)