import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Employee, Client

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/chatbot")
async def chatbot_query(question: dict, db: Session = Depends(get_db)):
    """
    Chatbot API to fetch employee, client, and sales (budget) data based on user questions.
    Example questions:
    - "How many employees do we have?"
    - "List all employee names."
    - "How many clients do we have?"
    - "List all client names."
    - "How many employees and clients do we have?"
    - "What is the total sales?"
    """
    query_text = question.get("question", "").lower()
    
    # Employees and Clients Count with Names
    if "how many employees and clients" in query_text:
        employees = db.query(Employee.name).all()
        clients = db.query(Client.name).all()
        
        employee_names = [emp.name for emp in employees]
        client_names = [cli.name for cli in clients]

        response = {
            "employee_count": len(employee_names),
            "employee_names": employee_names,
            "client_count": len(client_names),
            "client_names": client_names
        }
        return response

    # Employee-related queries
    if "how many employees" in query_text:
        employees = db.query(Employee.name).all()
        employee_names = [emp.name for emp in employees]
        return {"employee_count": len(employee_names), "employee_names": employee_names}
    
    if "list all employee names" in query_text:
        employees = db.query(Employee.name).all()
        employee_names = [emp.name for emp in employees]
        return {"employee_names": employee_names}

    # Client-related queries
    if "how many clients" in query_text:
        clients = db.query(Client.name).all()
        client_names = [cli.name for cli in clients]
        return {"client_count": len(client_names), "client_names": client_names}
    
    if "list all client names" in query_text:
        clients = db.query(Client.name).all()
        client_names = [cli.name for cli in clients]
        return {"client_names": client_names}

    # Sales-related queries (Using Client Budget as Total Sales)
    if "total sales" in query_text or "how much did we sell" in query_text:
        total_sales = db.query(Client.budget).all()
        total_amount = sum(client.budget for client in total_sales if client.budget is not None)
        return {"response": f"The total sales (budget from all clients) is ${total_amount:.2f}."}

    # Default response if the question is not understood
    return {"response": "I'm sorry, I don't understand that question."}