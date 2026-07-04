"""Role-based access control service."""
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)

class RBACService:
    ROLES = {
        "admin": ["*"],
        "manager": ["create_test", "run_tests", "view_reports", "edit_project"],
        "tester": ["run_tests", "view_reports"],
        "viewer": ["view_reports"],
    }

    async def verify_permission(self, user: dict, permission: str) -> bool:
        """Check if user has permission."""
        role = user.get("role", "viewer")
        allowed = self.ROLES.get(role, [])
        return "*" in allowed or permission in allowed

    async def assign_role(self, user_id: int, role: str) -> dict:
        """Assign role to user."""
        if role not in self.ROLES:
            return {"error": f"Invalid role: {role}"}
        return {"user_id": user_id, "role": role, "permissions": self.ROLES.get(role)}

    async def get_user_permissions(self, user: dict) -> list:
        """Get all permissions for user."""
        role = user.get("role", "viewer")
        return self.ROLES.get(role, [])
