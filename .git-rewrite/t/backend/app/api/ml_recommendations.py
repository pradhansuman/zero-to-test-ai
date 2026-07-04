"""ML-powered test recommendation API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.ml_recommender import MLRecommender
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ml", tags=["ml"])
logger = StructuredLogger(__name__)

class CodeChange(BaseModel):
    file: str
    module: str = ""

class RecommendationRequest(BaseModel):
    code_changes: list[CodeChange]
    top_k: int = 10

@router.post("/recommendations/{project_id}")
async def get_recommendations(
    project_id: int,
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get ML-based test recommendations for code changes."""
    try:
        recommender = MLRecommender(db)
        changes = [{"file": c.file, "module": c.module} for c in request.code_changes]
        result = await recommender.get_recommendations(project_id, changes, request.top_k)
        logger.info("recommendations_retrieved", project_id=project_id, count=len(result.get('recommendations', [])))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Recommendation generation failed")

@router.get("/predict-failure/{test_id}")
async def predict_failure(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Predict likelihood of test failure."""
    try:
        recommender = MLRecommender(db)
        prediction = await recommender.predict_failures(1, test_id)  # project_id=1 for now
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed")

@router.post("/train-model/{project_id}")
async def train_model(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Train ML model on project's historical data."""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin required")

        recommender = MLRecommender(db)
        result = await recommender.train_model(project_id)
        logger.info("model_trained", project_id=project_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Model training failed")
