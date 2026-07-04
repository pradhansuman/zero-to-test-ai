"""Analytics service for execution statistics and reporting."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
import json
import csv
from io import StringIO

from app.database.models import (
    Execution, ExecutionStatus, TestCase, ExecutionResult,
    Metric, DashboardConfig, CustomWidget
)
from app.repositories.execution import ExecutionRepository
from app.repositories.test_case import TestCaseRepository
from app.repositories.project import ProjectRepository
from app.exceptions import ProjectNotFound
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AnalyticsService:
    """Service for analytics and reporting."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.exec_repo = ExecutionRepository(session)
        self.test_repo = TestCaseRepository(session)
        self.project_repo = ProjectRepository(session)

    async def get_dashboard_stats(self, project_id: int) -> Dict[str, Any]:
        """Get dashboard statistics for project."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # Get all executions for project
            executions = await self.exec_repo.get_by_project(project_id, skip=0, limit=1000)

            if not executions:
                logger.info("No executions found", project_id=project_id)
                return {
                    "project_id": project_id,
                    "total_executions": 0,
                    "passed_executions": 0,
                    "failed_executions": 0,
                    "average_pass_rate": 0.0,
                    "average_duration": 0.0,
                    "flaky_test_count": 0
                }

            # Calculate statistics
            total = len(executions)
            passed = sum(1 for e in executions if e.status == ExecutionStatus.PASSED)
            failed = sum(1 for e in executions if e.status == ExecutionStatus.FAILED)
            avg_duration = sum(e.duration_seconds for e in executions) / total
            avg_pass_rate = sum(
                (e.passed / e.total_tests * 100) if e.total_tests > 0 else 0
                for e in executions
            ) / total

            # Get flaky test count (failure rate > 70%)
            flaky_count = await self._count_flaky_tests(project_id, threshold=0.7)

            dashboard = {
                "project_id": project_id,
                "total_executions": total,
                "passed_executions": passed,
                "failed_executions": failed,
                "average_pass_rate": round(avg_pass_rate, 2),
                "average_duration": round(avg_duration, 2),
                "flaky_test_count": flaky_count
            }

            logger.info(
                "Generated dashboard stats",
                project_id=project_id,
                total_executions=total,
                avg_pass_rate=avg_pass_rate
            )
            return dashboard
        except ProjectNotFound:
            raise
        except Exception as e:
            logger.error(
                f"Error getting dashboard stats: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def get_trends(
        self,
        project_id: int,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get execution trends over time."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # Get all executions
            executions = await self.exec_repo.get_by_project(project_id, skip=0, limit=10000)

            # Group by date
            from collections import defaultdict
            trends_by_date = defaultdict(lambda: {"tests": [], "pass_rate": 0, "count": 0})

            cutoff_date = datetime.utcnow() - timedelta(days=days)

            for execution in executions:
                if execution.created_at < cutoff_date:
                    continue

                date_key = execution.created_at.date()
                trends_by_date[date_key]["count"] += 1

                if execution.total_tests > 0:
                    pass_rate = (execution.passed / execution.total_tests) * 100
                    trends_by_date[date_key]["pass_rate"] += pass_rate
                    trends_by_date[date_key]["tests"].append(execution.total_tests)

            # Calculate daily averages
            trends = []
            for date_key in sorted(trends_by_date.keys()):
                data = trends_by_date[date_key]
                count = data["count"]
                avg_pass_rate = data["pass_rate"] / count if count > 0 else 0
                total_tests = sum(data["tests"])

                trends.append({
                    "date": str(date_key),
                    "pass_rate": round(avg_pass_rate, 2),
                    "test_count": total_tests,
                    "execution_count": count
                })

            logger.info(
                "Generated trends",
                project_id=project_id,
                days=days,
                trend_points=len(trends)
            )
            return trends
        except ProjectNotFound:
            raise
        except Exception as e:
            logger.error(
                f"Error getting trends: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def get_coverage(self, project_id: int) -> Dict[str, int]:
        """Get test coverage by type."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # Get all test cases for project
            test_cases = await self.test_repo.get_by_project(project_id, skip=0, limit=10000)

            # Count by type
            coverage = {
                "e2e": 0,
                "unit": 0,
                "integration": 0,
                "performance": 0,
                "total": len(test_cases)
            }

            for test_case in test_cases:
                test_type = test_case.test_type.lower()
                if test_type in coverage:
                    coverage[test_type] += 1

            logger.info(
                "Generated coverage stats",
                project_id=project_id,
                total_tests=coverage["total"]
            )
            return coverage
        except ProjectNotFound:
            raise
        except Exception as e:
            logger.error(
                f"Error getting coverage: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def get_flaky_tests(
        self,
        project_id: int,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Get flaky tests (high failure rate)."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # Get all test cases
            test_cases = await self.test_repo.get_by_project(project_id, skip=0, limit=10000)

            flaky_tests = []

            for test_case in test_cases:
                # Get all results for this test case
                from collections import defaultdict
                from sqlalchemy import select
                result = await self.session.execute(
                    select(Execution).where(Execution.project_id == project_id)
                )
                executions = result.scalars().all()

                # Count pass/fail for this test case
                total_runs = 0
                failures = 0

                for execution in executions:
                    for test_result in execution.results:
                        if test_result.test_case_id == test_case.id:
                            total_runs += 1
                            if test_result.status == ExecutionStatus.FAILED:
                                failures += 1

                if total_runs > 0:
                    failure_rate = failures / total_runs
                    if failure_rate >= threshold:
                        flaky_tests.append({
                            "test_case_id": test_case.id,
                            "test_case_name": test_case.name,
                            "failure_rate": round(failure_rate, 2),
                            "total_runs": total_runs,
                            "failures": failures
                        })

            # Sort by failure rate descending
            flaky_tests.sort(key=lambda x: x["failure_rate"], reverse=True)

            logger.info(
                "Generated flaky tests",
                project_id=project_id,
                flaky_count=len(flaky_tests),
                threshold=threshold
            )
            return flaky_tests
        except ProjectNotFound:
            raise
        except Exception as e:
            logger.error(
                f"Error getting flaky tests: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def _count_flaky_tests(self, project_id: int, threshold: float = 0.7) -> int:
        """Count flaky tests helper."""
        try:
            test_cases = await self.test_repo.get_by_project(project_id, skip=0, limit=10000)
            executions = await self.exec_repo.get_by_project(project_id, skip=0, limit=10000)

            flaky_count = 0

            for test_case in test_cases:
                total_runs = 0
                failures = 0

                for execution in executions:
                    for test_result in execution.results:
                        if test_result.test_case_id == test_case.id:
                            total_runs += 1
                            if test_result.status == ExecutionStatus.FAILED:
                                failures += 1

                if total_runs > 0:
                    failure_rate = failures / total_runs
                    if failure_rate >= threshold:
                        flaky_count += 1

            return flaky_count
        except Exception as e:
            logger.error(
                f"Error counting flaky tests: {str(e)}",
                error=str(e)
            )
            return 0

    async def record_metric(
        self,
        project_id: int,
        metric_type: str,
        value: float,
        tags: dict = None
    ) -> Dict[str, Any]:
        """Record a metric for real-time analytics (Phase 4)."""
        try:
            metric = Metric(
                project_id=project_id,
                metric_type=metric_type,
                value=value,
                tags=tags or {}
            )
            self.session.add(metric)
            await self.session.flush()
            logger.info("metric_recorded", project_id=project_id, metric_type=metric_type, value=value)
            return {
                'id': metric.id,
                'metric_type': metric_type,
                'value': value,
                'timestamp': metric.timestamp.isoformat()
            }
        except Exception as e:
            logger.error("metric_recording_error", error=str(e))
            return {"error": str(e)}

    async def get_realtime_metrics(
        self,
        project_id: int,
        metric_type: str,
        minutes: int = 60
    ) -> Dict[str, Any]:
        """Get real-time metrics aggregated over time window."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
            result = await self.session.execute(
                select(Metric)
                .where(
                    (Metric.project_id == project_id)
                    & (Metric.metric_type == metric_type)
                    & (Metric.timestamp >= cutoff_time)
                )
                .order_by(Metric.timestamp.desc())
            )
            metrics = result.scalars().all()
            if not metrics:
                return {'metric_type': metric_type, 'latest_value': 0, 'count': 0}
            values = [m.value for m in metrics]
            return {
                'metric_type': metric_type,
                'time_window_minutes': minutes,
                'latest_value': values[0] if values else 0,
                'average': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'count': len(metrics),
                'data_points': [{'timestamp': m.timestamp.isoformat(), 'value': m.value} for m in metrics]
            }
        except Exception as e:
            logger.error("realtime_metrics_error", error=str(e))
            return {"error": str(e)}

    async def get_trend_analysis(
        self,
        project_id: int,
        metric_type: str,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Calculate trend analysis for metric over period (Phase 4)."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=period_days)
            result = await self.session.execute(
                select(Metric)
                .where(
                    (Metric.project_id == project_id)
                    & (Metric.metric_type == metric_type)
                    & (Metric.timestamp >= cutoff_date)
                )
                .order_by(Metric.timestamp)
            )
            metrics = result.scalars().all()
            if not metrics:
                return {'metric_type': metric_type, 'trend': 'no_data', 'change_percent': 0}
            values = [m.value for m in metrics]
            average = sum(values) / len(values)
            mid = len(values) // 2
            first_half_avg = sum(values[:mid]) / max(mid, 1)
            second_half_avg = sum(values[mid:]) / max(len(values) - mid, 1)
            change_percent = (
                ((second_half_avg - first_half_avg) / max(first_half_avg, 0.001)) * 100
                if first_half_avg > 0 else 0
            )
            trend = 'improving' if change_percent < 0 else 'degrading' if change_percent > 0 else 'stable'
            return {
                'metric_type': metric_type,
                'period_days': period_days,
                'average': round(average, 3),
                'min': round(min(values), 3),
                'max': round(max(values), 3),
                'trend': trend,
                'change_percent': round(change_percent, 2),
                'data_points': len(metrics)
            }
        except Exception as e:
            logger.error("trend_analysis_error", error=str(e))
            return {"error": str(e)}

    async def create_dashboard(
        self,
        user_id: int,
        project_id: int,
        name: str,
        description: str = None,
        is_default: bool = False
    ) -> Dict[str, Any]:
        """Create custom dashboard configuration (Phase 4)."""
        try:
            dashboard = DashboardConfig(
                user_id=user_id,
                project_id=project_id,
                name=name,
                description=description,
                is_default=is_default,
                widgets=[]
            )
            self.session.add(dashboard)
            await self.session.flush()
            logger.info("dashboard_created", user_id=user_id, project_id=project_id, dashboard_id=dashboard.id)
            return {
                'id': dashboard.id,
                'name': name,
                'project_id': project_id,
                'created_at': dashboard.created_at.isoformat()
            }
        except Exception as e:
            logger.error("dashboard_creation_error", error=str(e))
            return {"error": str(e)}

    async def add_widget(
        self,
        dashboard_id: int,
        widget_type: str,
        title: str,
        metric_keys: list,
        time_range: str = "30d",
        config: dict = None
    ) -> Dict[str, Any]:
        """Add widget to dashboard (Phase 4)."""
        try:
            widget = CustomWidget(
                dashboard_id=dashboard_id,
                widget_type=widget_type,
                title=title,
                metric_keys=metric_keys,
                time_range=time_range,
                config=config or {}
            )
            self.session.add(widget)
            await self.session.flush()
            logger.info("widget_added", dashboard_id=dashboard_id, widget_type=widget_type)
            return {
                'id': widget.id,
                'widget_type': widget_type,
                'title': title,
                'dashboard_id': dashboard_id
            }
        except Exception as e:
            logger.error("widget_addition_error", error=str(e))
            return {"error": str(e)}

    async def get_dashboard(self, dashboard_id: int) -> Dict[str, Any]:
        """Get dashboard with all widgets (Phase 4)."""
        try:
            result = await self.session.execute(
                select(DashboardConfig)
                .where(DashboardConfig.id == dashboard_id)
                .options(joinedload(DashboardConfig.user))
            )
            dashboard = result.unique().scalar_one_or_none()
            if not dashboard:
                return {"error": "Dashboard not found"}
            widgets_result = await self.session.execute(
                select(CustomWidget).where(CustomWidget.dashboard_id == dashboard_id)
            )
            widgets = widgets_result.scalars().all()
            return {
                'id': dashboard.id,
                'name': dashboard.name,
                'description': dashboard.description,
                'project_id': dashboard.project_id,
                'user_id': dashboard.user_id,
                'is_default': dashboard.is_default,
                'created_at': dashboard.created_at.isoformat(),
                'widgets': [
                    {
                        'id': w.id,
                        'widget_type': w.widget_type,
                        'title': w.title,
                        'metric_keys': w.metric_keys,
                        'time_range': w.time_range,
                        'config': w.config
                    }
                    for w in widgets
                ]
            }
        except Exception as e:
            logger.error("dashboard_retrieval_error", error=str(e))
            return {"error": str(e)}

    async def export_metrics_csv(
        self,
        project_id: int,
        metric_type: str,
        days: int = 30
    ) -> str:
        """Export metrics as CSV (Phase 4)."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            result = await self.session.execute(
                select(Metric)
                .where(
                    (Metric.project_id == project_id)
                    & (Metric.metric_type == metric_type)
                    & (Metric.timestamp >= cutoff_date)
                )
                .order_by(Metric.timestamp)
            )
            metrics = result.scalars().all()
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['timestamp', 'value', 'tags'])
            for metric in metrics:
                writer.writerow([metric.timestamp.isoformat(), metric.value, json.dumps(metric.tags)])
            return output.getvalue()
        except Exception as e:
            logger.error("csv_export_error", error=str(e))
            return ""

    async def export_execution_report(
        self,
        project_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Export detailed execution report (Phase 4)."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            result = await self.session.execute(
                select(Execution)
                .where(
                    (Execution.project_id == project_id)
                    & (Execution.created_at >= cutoff_date)
                )
                .order_by(Execution.created_at.desc())
            )
            executions = result.scalars().all()
            execution_data = []
            for exe in executions:
                execution_data.append({
                    'id': exe.id,
                    'status': exe.status.value if exe.status else None,
                    'total_tests': exe.total_tests,
                    'passed': exe.passed,
                    'failed': exe.failed,
                    'skipped': exe.skipped,
                    'duration': exe.duration_seconds,
                    'started_at': exe.started_at.isoformat() if exe.started_at else None,
                    'ended_at': exe.ended_at.isoformat() if exe.ended_at else None,
                    'pass_rate': (exe.passed / exe.total_tests * 100) if exe.total_tests > 0 else 0
                })
            stats = await self.get_dashboard_stats(project_id)
            return {
                'project_id': project_id,
                'export_date': datetime.utcnow().isoformat(),
                'period_days': days,
                'summary': stats,
                'executions': execution_data
            }
        except Exception as e:
            logger.error("report_export_error", error=str(e))
            return {"error": str(e)}
