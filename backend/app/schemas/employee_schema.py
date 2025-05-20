 from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeCreate(BaseModel):
    name: str
    role: str
    salary: float
    joining_date: date
    dob: Optional[date] = None

    class Config:
        from_attributes = True

class EmployeeResponse(BaseModel):
    id: Optional[int]
    name: str
    role: str
    salary: float
    joining_date: date
    dob: Optional[date] = None

    class Config:
        from_attributes = True
