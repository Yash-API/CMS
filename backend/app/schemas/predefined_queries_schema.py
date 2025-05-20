from pydantic import BaseModel
from typing import Optional

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
