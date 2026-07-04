"""Pydantic schemas for AI agent endpoints."""
from pydantic import BaseModel
from typing import List, Optional


class GenerateTestsRequest(BaseModel):
    """Request to generate test cases."""
    description: str
    count: int = 5


class GeneratedTest(BaseModel):
    """Generated test case."""
    name: str
    description: str
    test_code: str
    test_type: str
    tags: List[str]
    confidence: float


class GenerateTestsResponse(BaseModel):
    """Generated tests response."""
    project_id: int
    generated_tests: List[GeneratedTest]
    count: int


class HealLocatorsRequest(BaseModel):
    """Request to heal broken locators."""
    execution_id: int
    screenshot: Optional[str] = None


class HealingAttempt(BaseModel):
    """Single healing attempt."""
    test_case_id: int
    old_selector: str
    new_selector: str
    confidence: float
    success: bool
    reason: str


class HealLocatorsResponse(BaseModel):
    """Healing results response."""
    execution_id: int
    healed_count: int
    healing_attempts: List[HealingAttempt]


class AnalyzeFailureRequest(BaseModel):
    """Request to analyze test failure."""
    execution_id: int
    test_case_id: int


class RelatedFailure(BaseModel):
    """Related failure information."""
    test_case_id: int
    test_case_name: str
    failure_type: str
    similarity_score: float


class AnalyzeFailureResponse(BaseModel):
    """Failure analysis response."""
    execution_id: int
    test_case_id: int
    failure_type: str
    root_cause: str
    suggestions: List[str]
    confidence: float
    related_failures: List[RelatedFailure]
