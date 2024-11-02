from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, select
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import httpx

DATABASE_URL = "sqlite:///./patients.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    details = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

async def fetch_patient(patient_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:32783/fhir/r4/Patient/{patient_id}")
        response.raise_for_status()
        return response.json()

@app.get("/patient/{patient_id}")
async def get_patient(patient_id: int):
    db = SessionLocal()
    try:
        patient = db.execute(select(Patient).filter(Patient.id == patient_id)).first()
        if patient:
            return patient[0]  # Return the patient object
        else:
            patient_data = await fetch_patient(patient_id)
            # Assume patient_data has 'id' and 'name' attributes
            new_patient = Patient(id=patient_data['id'], name=patient_data['name'], details=str(patient_data))
            db.add(new_patient)
            db.commit()
            db.refresh(new_patient)
            return new_patient
    finally:
        db.close()

@app.get("/patient")
async def get_all_patients():
    db = SessionLocal()
    try:
        patients = db.execute(select(Patient)).scalars().all()
        return patients
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
