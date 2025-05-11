from sqlalchemy import Column, Integer, String, Float, Date, BigInteger
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    salary = Column(Float)
    joining_date = Column(Date)
    dob = Column(Date, nullable=True)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    budget = Column(Float)
    project_description = Column(String, nullable=True)
    project_start_date = Column(Date)
    project_end_date = Column(Date, nullable=True)
    total_payment_received = Column(Integer, nullable=True)
    payment_received_account = Column(Integer, nullable=True)
    pending_payment = Column(Integer, nullable=True)

from sqlalchemy import ForeignKey

class ClientPayment(Base):
    __tablename__ = "client_payments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    payment_received_date = Column(Date)
    payment_received_amount = Column(Integer)


class PredefinedQueries(Base):
    __tablename__ = "predefined_queries"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    sql_query = Column(String, nullable=False)