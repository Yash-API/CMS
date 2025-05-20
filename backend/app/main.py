import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer 

load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, employees, clients, chatbot  # Import the chatbot router

# from app.utils.nlp_utils import llm  # Import llm to check its status

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Company Management System API",
    # Remove /api prefix as it's handled by nginx
    root_path=""
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.29.164:3000",  # Frontend URL
        "http://localhost:3000",        # Local development
        "http://127.0.0.1:3000"        # Alternative local URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])


# @app.post("/chatbot/")
# async def chatbot_endpoint(query: str):
#     response = chatbot_response(query)
#     return {"response": response}


@app.get("/")
def root():
    return {"message": "Welcome to the Company Management System API!"}
