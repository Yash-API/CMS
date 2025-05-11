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


class ClientCreate(BaseModel):
    name: str
    budget: Optional[float] = None
    project_description: Optional[str] = None
    project_start_date: Optional[date] = None
    project_end_date: Optional[date] = None
    total_payment_received: Optional[int] = None
    payment_received_account: Optional[int] = None
    pending_payment: Optional[int] = None

    class Config:
        from_attributes = True


class ClientResponse(BaseModel):
    id: Optional[int]
    name: str
    budget: Optional[float] = None
    project_description: Optional[str] = None
    project_start_date: Optional[date] = None
    project_end_date: Optional[date] = None
    total_payment_received: Optional[int] = None
    payment_received_account: Optional[int] = None
    pending_payment: Optional[int] = None

    class Config:
        from_attributes = True


class ClientPaymentCreate(BaseModel):
    client_id: int
    payment_received_date: date
    payment_received_amount: int

    class Config:
        from_attributes = True


class ClientPaymentResponse(BaseModel):
    id: Optional[int]
    client_id: int
    payment_received_date: date
    payment_received_amount: int

    class Config:
        from_attributes = True


class PredefinedQueriesCreate(BaseModel):
    question: str
    sql_query: str

    class Config:
        from_attributes = True


class PredefinedQueriesResponse(BaseModel):
    id: Optional[int]
    question: str
    sql_query: str

    class Config:
        from_attributes = True
