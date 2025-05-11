from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app import models, schemas, database
from passlib.context import CryptContext

router = APIRouter(prefix="/employees", tags=["Employees"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/employees/me")
def get_current_employee(employee: schemas.EmployeeResponse = Depends(get_current_user)):
    return employee


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    if not employee_id and not employee.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide employee ID or name for update"
        )
    db_employee = crud.update_employee(db, employee_id, employee)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return db_employee


@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    # Password hashing removed as Employee model does not have password field
    db_employee = models.Employee(
        name=employee.name,
        role=employee.role,
        salary=employee.salary,
        joining_date=employee.joining_date,
        dob=employee.dob
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/")
@router.get("/dashboard")
def get_employees_dashboard(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Retrieve all employees for the dashboard.
    Accessible by all authenticated users.
    """
    employees = db.query(models.Employee).all()

    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employees found"
        )

    return {"employees": employees}


def get_all_employees(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Extract user from JWT
):
    """
    Retrieve all employees from the database.
    Accessible by all authenticated users.
    """
    employees = db.query(models.Employee).all()

    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employees found"
        )

    return {"employees": employees}
