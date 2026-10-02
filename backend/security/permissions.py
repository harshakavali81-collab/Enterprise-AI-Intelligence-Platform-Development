from typing import List, Dict, Set

ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "EMPLOYEE": {
        "doc:read",
        "chat:use"
    },
    "ANALYST": {
        "doc:read",
        "chat:use",
        "sql:execute",
        "ml:predict",
        "analytics:view"
    },
    "MANAGER": {
        "doc:read",
        "chat:use",
        "sql:execute",
        "ml:predict",
        "analytics:view",
        "reports:generate",
        "workflow:approve"
    },
    "ADMIN": {
        "*" # Superuser wildcard
    }
}

def has_permission(user_role: str, required_permission: str) -> bool:
    role = user_role.upper()
    perms = ROLE_PERMISSIONS.get(role, set())
    if "*" in perms:
        return True
    return required_permission in perms

def enforce_permission(user_role: str, required_permission: str):
    if not has_permission(user_role, required_permission):
        raise PermissionError(
            f"Access Denied: Role '{user_role}' lacks required permission '{required_permission}'."
        )
