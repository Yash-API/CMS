import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.utils.security import create_access_token, verify_password, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import Employee, Client

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Attempting to log in user: {form_data.username} with contact/email")

    # Try to authenticate as employee first
    user = db.query(Employee).filter(
        (Employee.name == form_data.username)
    ).first()
    
    if not user:
        # Try to authenticate as client
        user = db.query(Client).filter(
            (Client.name == form_data.username)
        ).first()

    if not user:
        logger.warning(f"User not found: {form_data.username}. Invalid login attempt. Please check the contact/email.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Login successful for user: {form_data.username} without password verification")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    role = "employee" if isinstance(user, Employee) else "client"

    access_token = create_access_token(
        data={"sub": form_data.username, "role": role},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role
    }

@router.get("/dashboard")
async def dashboard(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    clients = db.query(Client).all()
    employees = db.query(Employee).all()
    return {"clients": clients, "employees": employees}
