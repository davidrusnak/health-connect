# main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from schemas import RequestBase
from database import get_request, get_requests_for_patient
from models import RequestorType
from schemas import RequestSchema
from models import RequestType
from database import SessionLocal, assign_parent, create_doctor, get_all_doctors, get_all_patients, get_doctor, init_db, \
    save_request
from schemas import AssignParent, DoctorCreate, DoctorSchema, PatientCreate, DocumentCreate, PatientDocumentAccessCreate, DocumentSchema, PatientSchema
from database import create_document, create_patient, assign_document_to_patient, get_patient, get_document

async def lifespan(app: FastAPI):
    # Startup action: Initialize the database
    await init_db()
    yield
    # Shutdown action: Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

# Dependency to get a new database session for each request
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/patients/", response_model=PatientSchema)
async def create_new_patient(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await create_patient(db, patient)

@app.post("/requests")
async def create_new_request(
    db: AsyncSession = Depends(get_db),
    requestor_type: RequestorType = Form(),
    from_id: int = Form(),
    to_id: int = Form(),
    request_type: RequestType = Form(),
    text: str = Form(),
    file: UploadFile = File(...),   # Get the uploaded file
):
    request_base = RequestBase(request_type = request_type, requestor_type = requestor_type, from_id = from_id, to_id = to_id, text = text)
    request = await save_request(db, request_base, file)
    return request

@app.get("/requests/{request_id}")
async def _get_request(request_id: int, db: AsyncSession = Depends(get_db)):
    result = await get_request(db, request_id)
    if not result:
        raise HTTPException(status_code=404, detail="Request not found")

    if result is not None:

        return FileResponse(result.image_path, media_type='application/octet-stream', headers={
            "Content-Disposition": f"attachment; filename={result.image_path.split('/')[-1]}"
        })

@app.get("/patients/{patient_id}/requests", response_model=list[RequestSchema])
async def _get_requests_for_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    requests = await get_requests_for_patient(db, patient_id)
    return requests

@app.get("/doctors/{doctor_id}/requests", response_model=list[RequestSchema])
async def _get_requests_for_doctors(doctor_id: int, db: AsyncSession = Depends(get_db)):
    requests = await get_requests_for_patient(db, doctor_id)
    return requests


# get pacient with ID
@app.get("/patients/{patient_id}", response_model=PatientSchema)
async def get_patient_by_id(patient_id: int, db: AsyncSession = Depends(get_db)):
    patient = await get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Endpoint to assign a parent to an existing patient
@app.post("/patients/{patient_id}/assign-parent")
async def assign_parent_to_patient(patient_id: int, assign_data: AssignParent, db: AsyncSession = Depends(get_db)):
    patient = await get_patient(db, patient_id)
    parent = await get_patient(db, assign_data.parent_id)
    if not patient or not parent:
        raise HTTPException(status_code=404, detail="Patient or Parent not found")
    updated_patient = await assign_parent(db, patient_id, assign_data.parent_id)
    return updated_patient

@app.post("/documents/", response_model=DocumentSchema)
async def create_new_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await create_document(db, document)

@app.post("/assignments/")
async def assign_document(access: PatientDocumentAccessCreate, db: AsyncSession = Depends(get_db)):
    patient = await get_patient(db, access.patient_id)
    document = await get_document(db, access.document_id)
    if not patient or not document:
        raise HTTPException(status_code=404, detail="Patient or Document not found")
    return await assign_document_to_patient(db, access.patient_id, access.document_id)

@app.get("/patients/{patient_id}/documents/", response_model=List[DocumentSchema])
async def get_patient_documents(patient_id: int, db: AsyncSession = Depends(get_db)):
    patient = await get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient.documents

@app.get("/parents/{parent_id}/children-documents/", response_model=List[DocumentSchema])
async def get_parent_accessible_documents(parent_id: int, db: AsyncSession = Depends(get_db)):
    parent = await get_patient(db, parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    child_documents = []
    for child in parent.children:
        child_documents.extend(child.documents)
    return child_documents

# Endpoint to create a new doctor
@app.post("/doctors/", response_model=DoctorSchema)
async def create_new_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await create_doctor(db, doctor)

# Endpoint to get a doctor by ID
@app.get("/doctors/{doctor_id}", response_model=DoctorSchema)
async def get_doctor_by_id(doctor_id: int, db: AsyncSession = Depends(get_db)):
    doctor = await get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# Endpoint to list all doctors
@app.get("/doctors/", response_model=list[DoctorSchema])
async def list_all_doctors(db: AsyncSession = Depends(get_db)):
    return await get_all_doctors(db)

@app.get("/patients/", response_model=list[PatientSchema])
async def list_all_patients(db: AsyncSession = Depends(get_db)):
    return await get_all_patients(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)