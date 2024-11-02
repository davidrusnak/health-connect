from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between Users and Doctors
user_doctor_association = Table(
    'user_doctor',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('doctor_id', Integer, ForeignKey('doctor.id'))
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    phone_predial = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    responsible_users = Column(String)  # comma-separated list of user IDs

    doctors = relationship("Doctor", secondary=user_doctor_association, back_populates="patients")


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    titles = Column(String, nullable=False)

    patients = relationship("User", secondary=user_doctor_association, back_populates="doctors")
