# crud.py
import uuid

from fastapi import File
from flask import request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from schemas import RequestBase
from models import RequestModel
from models import Base
from models import DoctorModel, PatientModel, DocumentModel, PatientDocumentAccess
import schemas


DATABASE_URL = "sqlite+aiosqlite:///./health-connect.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Function to initialize the database (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_patient(db: AsyncSession, patient_id: int):
    result = await db.execute(select(PatientModel).filter(PatientModel.id == patient_id))
    return result.scalars().first()

async def get_request(db: AsyncSession, request_id: int):
    result = await db.execute(select(RequestModel).filter(RequestModel.id == request_id))

    request = result.scalars().first()
    print(request)
    if request is not None:
        return request
        # with open(request.image_path, "rb") as file:
        #     return request

    return None

async def get_requests_for_patient(db: AsyncSession, patient_id: int):
    result = await db.execute(select(RequestModel).filter(RequestModel.to_id == patient_id)
                              .union(select(RequestModel).filter(RequestModel.from_id == patient_id)))
    return result.all()

async def get_requests_for_doctors(db: AsyncSession, doctor_id: int):
    result = await db.execute(select(RequestModel).filter(RequestModel.to_id == doctor_id)
                              .union(select(RequestModel).filter(RequestModel.from_id == doctor_id)))
    return result.all()

# Function to assign a parent to a patient
async def assign_parent(db: AsyncSession, patient_id: int, parent_id: int):
    patient = await db.get(PatientModel, patient_id)
    parent = await db.get(PatientModel, parent_id)
    if not patient or not parent:
        return None  # Return None if either patient or parent doesn't exist
    
    patient.parent_id = parent_id
    await db.commit()
    await db.refresh(patient)
    return patient

async def get_document(db: AsyncSession, document_id: int):
    result = await db.execute(select(DocumentModel).filter(DocumentModel.id == document_id))
    return result.scalars().first()

async def assign_document_to_patient(db: AsyncSession, patient_id: int, document_id: int):
    access = PatientDocumentAccess(patient_id=patient_id, document_id=document_id)
    db.add(access)
    await db.commit()
    await db.refresh(access)
    return access

async def create_document(db: AsyncSession, document_data: schemas.DocumentCreate):
    db_document = DocumentModel(**document_data.model_dump())
    db.add(db_document)
    await db.commit()
    await db.refresh(db_document)
    return db_document

async def create_patient(db: AsyncSession, patient_data: schemas.PatientCreate):
    db_patient = PatientModel(**patient_data.model_dump())
    #db_patient.children = []
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

async def create_doctor(db: AsyncSession, doctor_data: schemas.DoctorCreate):
    db_doctor = DoctorModel(**doctor_data.model_dump())
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    return db_doctor

async def save_request(db: AsyncSession, request_base: RequestBase, file: File):
    contents = await file.read()
    extension = file.filename.split(".")[-1] if "." in file.filename else ""
    new_name = f"{uuid.uuid4()}.{extension}"
    path = f"files/{new_name}"
    with open(path, "wb") as f:
        f.write(contents)

    db_request = RequestModel(**request_base.model_dump(), image_path=path)
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request

# Function to get a doctor by ID
async def get_doctor(db: AsyncSession, doctor_id: int):
    result = await db.execute(select(DoctorModel).filter(DoctorModel.id == doctor_id))
    return result.scalars().first()

# Function to get all doctors
async def get_all_doctors(db: AsyncSession):
    result = await db.execute(select(DoctorModel))
    return result.scalars().all()

async def get_all_patients(db: AsyncSession):
    result = await db.execute(select(PatientModel))
    return result.scalars().all()
