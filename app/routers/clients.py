from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from datetime import datetime
from app.database import get_db
from app import schemas, models
from app.models import Client
from app.schemas import ClientCreate, ClientResponse
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

@router.post("/", response_model=schemas.ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    """
    Create a new client with proper validation and error handling.
    """
    try:
        # Validate dates
        if client.project_endingdate and client.project_startingdate:
            if client.project_endingdate < client.project_startingdate:
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

        # Check if client already exists
        existing_client = db.query(models.Client).filter(
            (models.Client.email == client.email) | 
            (models.Client.contact == client.contact)
        ).first()
        
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this email or contact already exists"
            )

        # Hash password and create client
        hashed_password = pwd_context.hash(client.password)
        
        # Create client object with validated data
        db_client = models.Client(
            name=client.name.strip(),  # Remove leading/trailing whitespace
            email=client.email.lower(),  # Normalize email
            contact=client.contact,
            project_name=client.project_name,
            role="client",
            deadline=client.deadline,
            budget=client.budget,
            project_description=client.project_description,
            project_startingdate=client.project_startingdate,
            project_endingdate=client.project_endingdate,
            hashed_password=hashed_password,
            # created_at=datetime.utcnow()  # Add creation timestamp
        )

        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        
        logger.info(f"Successfully created client: {client.email}")
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
