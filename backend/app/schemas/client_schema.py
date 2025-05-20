from pydantic import BaseModel
from typing import Optional
from datetime import date

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
