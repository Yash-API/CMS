from sqlalchemy.orm import Session
from app.models import Employee
from app.core.security import get_password_hash

def get_employees(db: Session):
    """
    Retrieve all employees from the database.
    """
    return db.query(Employee).all()

def add_employee(db: Session, employee_data):
    hashed_password = get_password_hash(employee_data.password)
    db_employee = Employee(**employee_data.dict(), hashed_password=hashed_password)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def modify_employee(db: Session, employee_id: int, employee_data):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None
    for key, value in employee_data.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee
