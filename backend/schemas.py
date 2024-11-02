from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class DoctorBase(BaseModel):
    id: int
    name: str
    surname: str
    titles: str

class UserBase(BaseModel):
    name: str
    surname: str
    gender: str
    date_of_birth: date
    address: str
    phone_predial: str
    phone: str
    email: EmailStr
    responsible_users: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    doctors: List[DoctorBase] = []

    class Config:
        from_attributes = True

class Doctor(DoctorBase):
    id: int
    users: List[UserBase] = []

    class Config:
        from_attributes = True

class DoctorCreate(DoctorBase):
    pass