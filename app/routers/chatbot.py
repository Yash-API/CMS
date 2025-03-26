from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Employee, Client
from app.utils.nlp_utils import extract_name, extract_department, extract_role
import spacy

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

nlp = spacy.load("en_core_web_sm")  # Load NLP model

@router.get("/")
def chatbot(query: str, db: Session = Depends(get_db)):
    doc = nlp(query.lower())
    words = set(token.text for token in doc)  # Convert query into a set of words for faster lookup

    # **1. How many employees do we have?**
    if "employees" in words or "employee" in words and "how" in words and "many" in words:
        count = db.query(func.count(Employee.id)).scalar()
        return {"response": f"There are {count} employees in the company."}

    # **2. How many clients do we have? Give me their names**
    elif "clients" in words or "client" in words and "how" in words and "many" in words:
        clients = db.query(Client.name).all()
        client_names = [client[0] for client in clients]  # Extract names
        count = len(client_names)
        return {"response": f"There are {count} clients: {', '.join(client_names)}." if client_names else "There are no clients yet."}

    # **3. What is the salary of [employee name]?**
    elif "salary" in words and "of" in words:
        person_name = extract_name(doc)
        if person_name:
            employee = db.query(Employee).filter(Employee.name.ilike(f"%{person_name}%")).first()
            if employee:
                return {"response": f"{employee.name}'s salary is {employee.salary}."}
            else:
                return {"response": f"Could not find an employee named {person_name}."}

    # **4. List all employees in [department]**
    elif "employees" in words and "in" in words:
        department = extract_department(doc)
        if department:
            employees = db.query(Employee.name).filter(Employee.department.ilike(f"%{department}%")).all()
            employee_names = [emp[0] for emp in employees]
            return {"response": f"Employees in {department} department: {', '.join(employee_names)}." if employee_names else f"No employees found in {department} department."}

    # **5. Who is working as [role]?**
    elif "who" in words and "working" in words and "as" in words:
        role = extract_role(doc)
        if role:
            employees = db.query(Employee.name).filter(Employee.role.ilike(f"%{role}%")).all()
            employee_names = [emp[0] for emp in employees]
            return {"response": f"Employees working as {role}: {', '.join(employee_names)}." if employee_names else f"No employees found working as {role}."}


    # **6. What is the budget of [client name]?**
    elif "budget" in words and "of" in words:
        client_name = extract_name(doc)
        if client_name:
            client = db.query(Client).filter(Client.name.ilike(f"%{client_name}%")).first()
            if client:
                return {"response": f"{client.name}'s budget is {client.budget}."}
            else:
                return {"response": f"Could not find a client named {client_name}."}
        
    elif "list" in words and "employees" in words and "names" in words:
        employees = db.query(Employee.name).all()
        employee_names = [emp[0] for emp in employees]
        return {"response": f"Employees: {', '.join(employee_names)}." if employee_names else "No employees found."}
    
    
    return {"response": "I'm sorry, I don't understand the question."}
