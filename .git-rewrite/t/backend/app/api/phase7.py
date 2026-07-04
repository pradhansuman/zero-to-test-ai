"""Phase 7 API Endpoints - 24 endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.phase7_services import *

router = APIRouter(prefix="/api/phase7", tags=["phase7"])

@router.get("/ai/recommendations/{project_id}")
async def recommend(project_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"recommendations": await RecommendationEngine().recommend_tests(project_id)}

@router.post("/collaboration/session")
async def create_collaboration(test_id: int, users: list, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await RealtimeCollaboration().create_session(test_id, users)

@router.post("/chat/query")
async def chat_query(question: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await AIChat().query(question, {})

@router.post("/integrations/jira/issue")
async def create_jira_issue(failure: dict, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await JiraIntegration().create_issue(failure)

@router.post("/integrations/slack/alert")
async def send_slack_alert(channel: str, message: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await SlackTeamsIntegration().send_alert(channel, message)

@router.post("/integrations/github/trigger")
async def trigger_github(workflow: str, inputs: dict, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await CIPipelineIntegration().trigger_github_action(workflow, inputs)

@router.post("/mobile/launch-ios")
async def launch_ios(app_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await MobileTestingSuite().launch_ios_simulator(app_id)

@router.post("/mobile/launch-android")
async def launch_android(app_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await MobileTestingSuite().launch_android_emulator(app_id)

@router.get("/sdk/ios/{version}")
async def get_ios_sdk(version: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await CrossPlatformSDK().get_ios_sdk(version)

@router.get("/performance/battery/{test_id}")
async def profile_battery(test_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await PerformanceProfiling().profile_battery(test_id)

@router.get("/dashboard/config")
async def get_dashboard(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await ReactDashboard().get_dashboard_config(current_user["id"])

@router.get("/docs/openapi")
async def get_openapi(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await DeveloperDocumentation().generate_openapi_spec()

@router.get("/guides/setup")
async def setup_guide(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await UserGuides().get_setup_guide()

@router.get("/faq/{category}")
async def get_faq(category: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"faqs": await UserGuides().get_faq(category)}
