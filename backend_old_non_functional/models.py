# models.py
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Table
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
    documents = relationship("DocumentModel", secondary="patient_document_access", back_populates="patients")
    #children = relationship("PatientModel", backref="parent", remote_side=[id])

class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    patients = relationship("PatientModel", secondary="patient_document_access", back_populates="documents")
