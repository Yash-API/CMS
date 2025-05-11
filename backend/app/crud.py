from sqlalchemy.orm import Session
from app.models import Employee, Client, ClientPayment
from app.utils.security import get_password_hash
from sqlalchemy.exc import SQLAlchemyError

def get_client_by_contact_or_email(db: Session, username: str, is_email: bool = False):
    return db.query(Client).filter((Client.contact == username) | (Client.email == username)).first()

def get_employee_by_contact_or_email(db: Session, username: str, is_email: bool = False):
    return db.query(Employee).filter((Employee.contact == username) | (Employee.email == username)).first()

def create_employee(db: Session, employee_data):
    hashed_password = get_password_hash(employee_data.password)
    db_employee = Employee(**employee_data.dict(), hashed_password=hashed_password)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def add_client_payment(db: Session, client_payment_data):
    try:
        # Create new client payment record
        new_payment = ClientPayment(
            client_id=client_payment_data.client_id,
            payment_received_date=client_payment_data.payment_received_date,
            payment_received_amount=client_payment_data.payment_received_amount
        )
        db.add(new_payment)

        # Update client's total_payment_received and pending_payment
        client = db.query(Client).filter(Client.id == client_payment_data.client_id).first()
        if client:
            if client.total_payment_received is None:
                client.total_payment_received = 0
            client.total_payment_received += client_payment_data.payment_received_amount

            if client.budget is not None:
                client.pending_payment = client.budget - client.total_payment_received
            else:
                client.pending_payment = None

            db.add(client)

        db.commit()
        db.refresh(new_payment)
        return new_payment
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_all_employees(db: Session):
    """
    Retrieve all employees from the database.
    """
    return db.query(Employee).all()

def update_employee(db: Session, employee_id: int, employee_data):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None
    for key, value in employee_data.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_client(db: Session, client_id: int, client_data):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return None
    for key, value in client_data.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client
