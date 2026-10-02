from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Dict, Any, List
from backend.database.schemas import LoginRequest, TokenResponse, UserResponse
from backend.security.auth import create_access_token, verify_token, verify_password, hash_password
from backend.database.connection import DatabaseConnection

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Predefined users for quick demo & testing
USERS_DB = {
    "admin": {"user_id": 1, "username": "admin", "password_hash": "admin123", "role": "ADMIN", "department": "Executive", "full_name": "Chief AI Officer", "email": "admin@enterprise.ai"},
    "manager_priya": {"user_id": 2, "username": "manager_priya", "password_hash": "manager123", "role": "MANAGER", "department": "Sales", "full_name": "Priya Sharma", "email": "priya.sharma@enterprise.ai"},
    "analyst_rahul": {"user_id": 3, "username": "analyst_rahul", "password_hash": "analyst123", "role": "ANALYST", "department": "Analytics", "full_name": "Rahul Verma", "email": "rahul.verma@enterprise.ai"},
    "employee_ananya": {"user_id": 4, "username": "employee_ananya", "password_hash": "employee123", "role": "EMPLOYEE", "department": "Operations", "full_name": "Ananya Rao", "email": "ananya.rao@enterprise.ai"}
}

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        # Default fallback for interactive API testing
        return USERS_DB["admin"]
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired JWT token")
    username = payload.get("sub")
    if username in USERS_DB:
        return USERS_DB[username]
    return {"user_id": payload.get("user_id", 1), "username": username, "role": payload.get("role", "EMPLOYEE"), "department": payload.get("department", "General")}

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = USERS_DB.get(req.username)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "sub": user["username"],
        "user_id": user["user_id"],
        "role": user["role"],
        "department": user["department"]
    })

    return TokenResponse(
        access_token=token,
        username=user["username"],
        role=user["role"],
        user_id=user["user_id"],
        department=user["department"]
    )

@router.get("/me")
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    return current_user

@router.get("/users", response_model=List[UserResponse])
def list_users(current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden: Listing users requires ADMIN role.")
    return [
        UserResponse(
            user_id=u["user_id"],
            username=u["username"],
            email=u["email"],
            full_name=u["full_name"],
            department=u["department"],
            role_name=u["role"],
            is_active=True
        )
        for u in USERS_DB.values()
    ]
