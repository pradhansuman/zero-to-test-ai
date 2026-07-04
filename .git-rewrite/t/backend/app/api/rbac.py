"""RBAC management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.services.rbac_service import RBACService
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/rbac", tags=["rbac"])
logger = StructuredLogger(__name__)

@router.post("/assign-role/{user_id}")
async def assign_role(
    user_id: int,
    role: str,
    current_user: dict = Depends(get_current_user),
):
    """Assign role to user (admin only)."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    service = RBACService()
    result = await service.assign_role(user_id, role)
    logger.info("role_assigned", user_id=user_id, role=role)
    return result

@router.get("/permissions")
async def get_permissions(current_user: dict = Depends(get_current_user)):
    """Get current user permissions."""
    service = RBACService()
    permissions = await service.get_user_permissions(current_user)
    return {"permissions": permissions}
