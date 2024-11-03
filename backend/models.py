# models.py
from enum import Enum
from typing import List

from fastapi import File
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum as SaEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for many-to-many relationship between Patient and Document
class PatientDocumentAccess(Base):
    __tablename__ = "patient_document_access"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))

class DoctorModel(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class PatientModel(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    #parents_id = Column(List(Integer), ForeignKey("patients.id"), nullable=True)
    documents = relationship("DocumentModel", secondary="patient_document_access", back_populates="patients", lazy="selectin")
    #children = relationship("PatientModel", backref="parent", remote_side=[id])

class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    patients = relationship("PatientModel", secondary="patient_document_access", back_populates="documents", lazy="selectin")

class RequestType(Enum):
    DrugReq = "Drug Request"
    AppointmentReq = "Appointment Request"

class RequestorType(Enum):
    Doctor = "Doctor"
    Patient = "Patient"

class RequestModel(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    requestor_type = Column(SaEnum(RequestorType))
    from_id = Column(Integer)
    to_id = Column(Integer)
    # img_type = Column(String)
    image_path = Column(String, index=True)
    request_type = Column(SaEnum(RequestType))
    text = Column(String)
