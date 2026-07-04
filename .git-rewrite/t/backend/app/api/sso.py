"""SSO integration API endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.sso_service import SSOService
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/auth/sso", tags=["sso"])
logger = StructuredLogger(__name__)

class OAuthCallback(BaseModel):
    code: str
    provider: str

@router.post("/google/callback")
async def google_callback(callback: OAuthCallback):
    """Google OAuth callback."""
    try:
        service = SSOService()
        token = await service.exchange_google_code(callback.code)
        if "error" in token:
            raise HTTPException(status_code=400, detail=token["error"])
        logger.info("google_sso_success")
        return token
    except Exception as e:
        raise HTTPException(status_code=500, detail="OAuth failed")

@router.post("/github/callback")
async def github_callback(callback: OAuthCallback):
    """GitHub OAuth callback."""
    try:
        service = SSOService()
        token = await service.exchange_github_code(callback.code)
        if "error" in token:
            raise HTTPException(status_code=400, detail=token["error"])
        logger.info("github_sso_success")
        return token
    except Exception as e:
        raise HTTPException(status_code=500, detail="OAuth failed")
