from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from datetime import datetime
from app.database import get_db
from app import schemas, models, crud
from app.models import Client
from app.schemas import ClientCreate, ClientResponse, ClientPaymentCreate, ClientPaymentResponse
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.get("/", response_model=List[ClientResponse])
@router.get("/dashboard", response_model=List[ClientResponse])
def get_clients_dashboard(db: Session = Depends(get_db)):
    """
    Retrieve all clients for the dashboard.
    """
    try:
        return db.query(Client).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving clients"
        )

@router.put("/{client_id}", response_model=schemas.ClientResponse)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    if not client_id and not client.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide client ID or name for update"
        )
    db_client = crud.update_client(db, client_id, client)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return db_client

@router.post("/", response_model=schemas.ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    """
    Create a new client with proper validation and error handling.
    """
    try:
        # Validate dates
        if client.project_end_date and client.project_start_date:
            if client.project_end_date < client.project_start_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Project end date cannot be before start date"
                )

        # Validate budget
        if client.budget and client.budget < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Budget cannot be negative"
            )

        # Create client object with validated data
        db_client = models.Client(
            name=client.name.strip(),  # Remove leading/trailing whitespace
            budget=client.budget,
            project_description=client.project_description,
            project_start_date=client.project_start_date,
            project_end_date=client.project_end_date,
            total_payment_received=client.total_payment_received,
            payment_received_account=client.payment_received_account,
            pending_payment=client.pending_payment,
        )

        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        
        logger.info(f"Successfully created client: {client.name}")
        return db_client

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating client"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid input data"
        )

@router.post("/payments", response_model=ClientPaymentResponse, status_code=status.HTTP_201_CREATED)
def add_client_payment(payment: ClientPaymentCreate, db: Session = Depends(get_db)):
    """
    Add a payment for a client and update the client's total and pending payments.
    """
    try:
        new_payment = crud.add_client_payment(db, payment)
        logger.info(f"Added payment of amount {payment.payment_received_amount} for client ID {payment.client_id}")
        return new_payment
    except SQLAlchemyError as e:
        logger.error(f"Database error while adding client payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while adding client payment"
        )
    except Exception as e:
        logger.error(f"Unexpected error while adding client payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid input data"
        )
