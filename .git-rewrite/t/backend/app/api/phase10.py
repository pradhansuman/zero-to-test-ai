"""Phase 10 API Endpoints - 18 endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.phase10_services import *

router = APIRouter(prefix="/api/phase10", tags=["phase10"])

@router.post("/ai/llm/openai")
async def generate_openai(prompt: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"response": await LLMIntegration().generate_with_openai(prompt)}

@router.post("/ai/generation/screenshot")
async def gen_from_screenshot(image_path: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await TestGenerationV3().generate_test_from_screenshot(image_path)

@router.post("/ai/generation/self-healing")
async def gen_self_healing(requirements: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await TestGenerationV3().generate_self_healing_test(requirements)

@router.post("/ai/analysis/screenshot")
async def analyze_screenshot(image_path: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await FailureAnalysisV2().analyze_screenshot(image_path)

@router.post("/ai/analysis/video")
async def analyze_video(video_path: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await FailureAnalysisV2().analyze_video(video_path)

@router.post("/ai/bug-report/jira")
async def generate_jira(failure: dict, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await AutoBugReportGeneration().generate_jira_issue(failure)

@router.post("/ai/bug-report/github")
async def generate_github(failure: dict, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await AutoBugReportGeneration().generate_github_issue(failure)

@router.post("/ai/bug-report/suggest-fix")
async def suggest_fix(failure: dict, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"suggestion": await AutoBugReportGeneration().suggest_fix(failure)}

@router.post("/ai/knowledge/ingest")
async def ingest_knowledge(documents: list, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await KnowledgeBaseIntegration().ingest_documents(documents)

@router.post("/ai/knowledge/retrieve")
async def retrieve_knowledge(query: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"results": await KnowledgeBaseIntegration().retrieve_similar(query)}

@router.post("/ai/chat")
async def chat(message: str, conversation_id: str = "", db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"response": await ConversationalAI().chat(message, {})}

@router.post("/ai/chat/command")
async def execute_ai_command(command: str, args: list = [], db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await ConversationalAI().execute_command(command, args)
