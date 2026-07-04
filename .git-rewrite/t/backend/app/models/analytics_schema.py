"""Pydantic schemas for analytics endpoints."""
from pydantic import BaseModel
from typing import List, Dict
from datetime import date


class DashboardStats(BaseModel):
    """Dashboard statistics response."""
    project_id: int
    total_executions: int
    passed_executions: int
    failed_executions: int
    average_pass_rate: float
    average_duration: float
    flaky_test_count: int


class TrendPoint(BaseModel):
    """Single trend data point."""
    date: str
    pass_rate: float
    test_count: int
    execution_count: int


class TrendsResponse(BaseModel):
    """Trends response."""
    project_id: int
    days: int
    trends: List[TrendPoint]


class CoverageStats(BaseModel):
    """Test coverage statistics."""
    e2e: int
    unit: int
    integration: int
    performance: int
    total: int


class CoverageResponse(BaseModel):
    """Coverage response."""
    project_id: int
    coverage: CoverageStats


class FlakyTest(BaseModel):
    """Flaky test information."""
    test_case_id: int
    test_case_name: str
    failure_rate: float
    total_runs: int
    failures: int


class FlakyTestsResponse(BaseModel):
    """Flaky tests response."""
    project_id: int
    threshold: float
    flaky_tests: List[FlakyTest]
    count: int

    class Config:
        from_attributes = True
