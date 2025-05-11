from fastapi import APIRouter, Depends
from app.dependencies import require_role

router = APIRouter(
    prefix="/protected",
    tags=["Protected Routes"]
)

# 🛡️ Admin-only access
@router.get("/admin/dashboard")
async def admin_dashboard(user: dict = Depends(require_role("admin"))):
    return {
        "message": "Welcome to admin dashboard",
        "user": user
    }

# 🛡️ Client-only access
@router.get("/client/dashboard")
async def client_dashboard(user: dict = Depends(require_role("client"))):
    return {
        "message": "Welcome to client dashboard",
        "user": user
    }

# 🛡️ Employee-only access
@router.get("/employee/dashboard")
async def employee_dashboard(user: dict = Depends(require_role("employee"))):
    return {
        "message": "Welcome to employee dashboard",
        "user": user
    }
