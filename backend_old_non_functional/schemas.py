# schemas.py
from fastapi import File
from pydantic import BaseModel, Field
from typing import List, Optional

from backend_old_non_functional.models import RequestModel
from models import RequestType, RequestorType


class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentSchema(DocumentBase):
    id: int

    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str

class PatientCreate(PatientBase):
    pass

class PatientSchema(PatientBase):
    id: int
    documents: List["DocumentSchema"] = []
    children: List["PatientSchema"] = []

    class Config:
        from_attributes = True

class AssignParent(BaseModel):
    parent_id: int

class PatientDocumentAccessCreate(BaseModel):
    patient_id: int
    document_id: int

class DoctorBase(BaseModel):
    name: str

class DoctorCreate(DoctorBase):
    pass

class DoctorSchema(DoctorBase):
    id: int

    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    requestor_type: RequestorType
    from_id: int
    to_id: int
    request_type: RequestType
    text: str

class RequestCreate(RequestBase):
    pass

class RequestSchema(RequestBase):
    id: int
    image_path: str

    class Config:
        from_attributes = True
        use_enum_values = True
