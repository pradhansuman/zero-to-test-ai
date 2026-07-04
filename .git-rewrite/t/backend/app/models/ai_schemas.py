"""Pydantic schemas for AI features."""
from pydantic import BaseModel, Field
from typing import Optional


class GenerateTestRequest(BaseModel):
    """Request to generate a test case."""

    story_description: str = Field(..., description="User story or requirement")
    acceptance_criteria: Optional[str] = Field(None, description="Acceptance criteria")
    framework: str = Field("pytest", description="Testing framework")
    test_type: str = Field("functional", description="Type of test")


class GenerateAPITestRequest(BaseModel):
    """Request to generate an API test."""

    endpoint: str = Field(..., description="API endpoint")
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")
    expected_response: Optional[str] = Field(None, description="Expected response format")


class GenerateUITestRequest(BaseModel):
    """Request to generate a UI test."""

    user_flow: str = Field(..., description="Description of user flow")
    page_url: Optional[str] = Field(None, description="URL to test")
    elements_to_interact: Optional[list] = Field(None, description="Elements to interact with")


class HealLocatorRequest(BaseModel):
    """Request to heal a broken locator."""

    broken_selector: str = Field(..., description="Current broken selector")
    element_description: str = Field(..., description="Description of element to find")
    html_snippet: Optional[str] = Field(None, description="HTML context around element")


class AnalyzeFailureRequest(BaseModel):
    """Request to analyze a test failure."""

    error_message: str = Field(..., description="Error message")
    test_name: str = Field(..., description="Name of failing test")
    stack_trace: Optional[str] = Field(None, description="Stack trace")


class OptimizeTestRequest(BaseModel):
    """Request to optimize test code."""

    test_code: str = Field(..., description="Test code to optimize")
    framework: str = Field("pytest", description="Testing framework")


class GeneratedTestResponse(BaseModel):
    """Response with generated test."""

    test_code: str
    test_type: str
    framework: str
    generated_by: str
    model: str


class TestImprovementResponse(BaseModel):
    """Response with test improvement suggestions."""

    suggestions: str
    optimized_by: str
    framework: str


class LocatorHealResponse(BaseModel):
    """Response with healed locator."""

    suggested_selector: str
    explanation: str
    confidence: float
    healed_by: str


class FailureAnalysisResponse(BaseModel):
    """Response with failure analysis."""

    analysis: str
    failure_type: str
    test_name: str
    analyzed_by: str


class BatchGenerateRequest(BaseModel):
    """Request to generate multiple tests."""

    stories: list[str] = Field(..., description="List of story descriptions")
    framework: str = Field("pytest", description="Testing framework")
