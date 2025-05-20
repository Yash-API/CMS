from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user

def require_role(expected_role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        if user["role"] != expected_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {user['role']}"
            )
        return user
    return role_dependency
