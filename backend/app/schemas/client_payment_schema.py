from pydantic import BaseModel
from typing import Optional
from datetime import date

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
