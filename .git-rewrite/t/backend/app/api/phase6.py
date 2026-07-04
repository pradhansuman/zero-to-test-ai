"""Phase 6 API Endpoints - 18 endpoints for 12 tasks."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.phase6_services import (
    MonitoringService, LoggingService, IncidentService,
    SDKService, CLIService, IDEIntegrationService,
    DataPipelineService, AnalyticsService, DataGovernanceService,
    ComplianceService, WorkspaceService, WorkflowAutomationService
)

router = APIRouter(prefix="/api/phase6", tags=["phase6"])

# TIER 1: OBSERVABILITY
@router.get("/monitoring/metrics/{service}")
async def get_metrics(service: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = MonitoringService()
    return await service_obj.collect_metrics(service)

@router.get("/monitoring/traces/{request_id}")
async def get_traces(request_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = MonitoringService()
    return await service_obj.get_traces(request_id)

@router.post("/logging/search")
async def search_logs(query: str, start_time: str, end_time: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = LoggingService()
    return {"logs": await service_obj.search_logs(query, start_time, end_time)}

@router.post("/incidents/create")
async def create_incident(title: str, severity: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = IncidentService()
    return await service_obj.create_incident(title, severity)

@router.get("/incidents/oncall")
async def get_oncall(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = IncidentService()
    return await service_obj.get_oncall_schedule()

# TIER 2: DEVELOPER EXPERIENCE
@router.get("/sdk/versions/{language}")
async def get_sdk_versions(language: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = SDKService()
    return await service_obj.get_sdk_versions(language)

@router.get("/sdk/stats/{language}")
async def get_sdk_stats(language: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = SDKService()
    return await service_obj.get_sdk_stats(language)

@router.get("/cli/docs/{command}")
async def get_cli_docs(command: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = CLIService()
    return await service_obj.get_cli_docs(command)

@router.get("/cli/api-reference")
async def generate_api_reference(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = CLIService()
    return await service_obj.generate_api_reference()

@router.get("/ide/vscode")
async def get_vscode_extension(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = IDEIntegrationService()
    return await service_obj.get_vs_code_extension()

@router.get("/ide/lsp/{file_path:path}")
async def get_lsp_diagnostics(file_path: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = IDEIntegrationService()
    return {"diagnostics": await service_obj.get_lsp_diagnostics(file_path)}

# TIER 3: DATA & ANALYTICS
@router.post("/data/pipeline/sync")
async def sync_to_warehouse(source: str, destination: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = DataPipelineService()
    return await service_obj.sync_to_warehouse(source, destination)

@router.post("/analytics/query")
async def execute_olap(query: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = AnalyticsService()
    return await service_obj.execute_olap_query(query)

@router.post("/analytics/drilldown")
async def drill_down(dimension: str, value: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = AnalyticsService()
    return await service_obj.drill_down(dimension, value)

@router.get("/governance/lineage/{dataset_id}")
async def get_lineage(dataset_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = DataGovernanceService()
    return await service_obj.track_lineage(dataset_id)

@router.get("/governance/catalog")
async def search_catalog(query: str = "", db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = DataGovernanceService()
    return {"datasets": await service_obj.get_data_catalog(query)}

# TIER 4: COMPLIANCE & ENTERPRISE
@router.get("/compliance/soc2/{control_id}")
async def check_soc2(control_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = ComplianceService()
    return await service_obj.check_soc2_compliance(control_id)

@router.get("/compliance/hipaa-report")
async def get_hipaa_report(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = ComplianceService()
    return await service_obj.get_hipaa_report()

@router.post("/workspace/create")
async def create_workspace(name: str, organization_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = WorkspaceService()
    return await service_obj.create_workspace(name, organization_id)

@router.post("/workflow/create")
async def create_workflow(name: str, steps: list, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = WorkflowAutomationService()
    return await service_obj.create_workflow(name, steps)

@router.post("/workflow/execute/{workflow_id}")
async def execute_workflow(workflow_id: str, trigger_data: dict = None, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service_obj = WorkflowAutomationService()
    return await service_obj.execute_workflow(workflow_id, trigger_data or {})
