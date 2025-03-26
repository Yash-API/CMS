from datetime import date
from typing import Optional, Pattern
from pydantic import BaseModel, EmailStr, constr, validator

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    contact: int
    department: str
    role: str
    salary: float
    joining_date: date
    leave_date: Optional[date] = None
    attendance: Optional[str] = None
    holidays: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    contact: int
    role: Optional[str] = "client"  # Default role set to "client"
    project_name: str
    deadline: date  # Changed from str to date for proper validation
    budget: float
    project_description: Optional[str] = None
    project_startingdate: date
    project_endingdate: Optional[date] = None

    @validator('contact')
    def validate_contact(cls, v):
        if len(str(v)) != 10:
            raise ValueError('Contact number must be exactly 10 digits')
        return v

    @validator('project_startingdate')
    def validate_start_date(cls, v):
        if v < date.today():
            raise ValueError('Project start date cannot be in the past')
        return v

    @validator('project_endingdate')
    def validate_end_date(cls, v, values):
        if 'project_startingdate' in values and v:
            if v <= values['project_startingdate']:
                raise ValueError('Project end date must be after start date')
        return v

class ClientCreate(ClientBase):
    password: str

class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True