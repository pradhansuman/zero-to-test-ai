"""
shared/contracts/engine_schemas.py
──────────────────────────────────
Pydantic models for Phase 1 testing engines (API & Database).
These schemas define the contract between the orchestrator and each engine.

Each engine accepts TEST_CASE models and returns RESULT models.
This separation enables independent testing, mocking, and versioning.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional, Dict, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


# ─────────────────────── Enums ───────────────────────


class HTTPMethod(str, Enum):
    """HTTP request methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AssertionType(str, Enum):
    """Assertion comparison types."""
    EQUALS = "equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN_OR_EQUAL = "lte"
    MATCHES_REGEX = "regex"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    IN_LIST = "in"
    NOT_IN_LIST = "not_in"
    LENGTH_EQUALS = "length_eq"
    TYPE_EQUALS = "type_eq"


class TestStatus(str, Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class AuthType(str, Enum):
    """Authentication types for API testing."""
    NONE = "none"
    BEARER = "bearer"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    CUSTOM = "custom"


class ConstraintType(str, Enum):
    """Database constraint types."""
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"
    NOT_NULL = "not_null"
    CHECK = "check"
    DEFAULT = "default"


# ─────────────────────── Assertion Models ───────────────────────


class Assertion(BaseModel):
    """Single assertion to validate in a test."""
    type: AssertionType = Field(..., description="Assertion comparison type")
    target: str = Field(..., description="Path to value: 'status_code', 'body.user.name', etc.")
    expected: Any = Field(..., description="Expected value")
    error_message: Optional[str] = Field(None, description="Custom error message on failure")

    @validator("target")
    def validate_target(cls, v: Any) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("target must be a non-empty string")
        return v


# ─────────────────────── API Testing Models ───────────────────────


class APIHeader(BaseModel):
    """HTTP header."""
    name: str
    value: str
    sensitive: bool = Field(False, description="Mask in logs if True")


class APIAuth(BaseModel):
    """Authentication configuration."""
    type: AuthType = AuthType.NONE
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    api_key: Optional[str] = None
    header_name: Optional[str] = None


class APITestCase(BaseModel):
    """Single API test case (REST or GraphQL)."""
    id: str = Field(..., description="Unique test ID, e.g., 'API-001'")
    name: str = Field(..., description="Test name")
    description: Optional[str] = None
    method: HTTPMethod = HTTPMethod.GET
    endpoint: str = Field(..., description="URL path or full URL")
    headers: Dict[str, str] = Field(default_factory=dict)
    auth: Optional[APIAuth] = None
    query_params: Dict[str, str] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    timeout: int = Field(30, description="Request timeout in seconds")
    assertions: List[Assertion] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    skip: bool = False

    @validator("endpoint")
    def validate_endpoint(cls, v: Any) -> str:
        if not v:
            raise ValueError("endpoint cannot be empty")
        return v


class GraphQLTestCase(BaseModel):
    """GraphQL query/mutation test case."""
    id: str = Field(..., description="Unique test ID")
    name: str
    description: Optional[str] = None
    query: str = Field(..., description="GraphQL query or mutation")
    variables: Optional[Dict[str, Any]] = None
    operation_name: Optional[str] = None
    auth: Optional[APIAuth] = None
    endpoint: str
    timeout: int = Field(30)
    assertions: List[Assertion] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    skip: bool = False


class ContractValidationCase(BaseModel):
    """OpenAPI/Swagger contract validation test."""
    id: str
    name: str
    openapi_spec_url: str = Field(..., description="URL to OpenAPI spec")
    test_cases: List[APITestCase] = Field(..., description="Cases to validate against spec")
    tags: List[str] = Field(default_factory=list)


class APITestResult(BaseModel):
    """Result of executing a single API test."""
    test_id: str
    test_name: str
    status: TestStatus
    method: HTTPMethod
    endpoint: str
    request_headers: Dict[str, str]
    request_body: Optional[Dict[str, Any]]
    response_status_code: Optional[int]
    response_headers: Optional[Dict[str, str]]
    response_body: Optional[Any]
    response_time_ms: float
    assertions_passed: int
    assertions_failed: int
    error_message: Optional[str]
    stack_trace: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == TestStatus.PASSED

    @property
    def assertion_success_rate(self) -> float:
        total = self.assertions_passed + self.assertions_failed
        return (self.assertions_passed / total * 100) if total > 0 else 0.0


class APIExecutionSummary(BaseModel):
    """Summary of API test execution."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    error_rate: float = Field(..., description="Percentage of tests with errors")
    average_response_time_ms: float
    execution_time_seconds: float
    results: List[APITestResult]

    @property
    def success_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return (self.passed / self.total_tests) * 100


# ─────────────────────── Database Testing Models ───────────────────────


class DatabaseColumn(BaseModel):
    """Column definition in a table."""
    name: str
    type: str = Field(..., description="e.g., 'INTEGER', 'VARCHAR', 'TIMESTAMP'")
    nullable: bool = True
    default: Optional[str] = None
    constraints: List[ConstraintType] = Field(default_factory=list)


class SQLTestCase(BaseModel):
    """Single SQL test case."""
    id: str = Field(..., description="Unique test ID, e.g., 'DB-001'")
    name: str
    description: Optional[str] = None
    sql: str = Field(..., description="SQL query or statement")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    expected_row_count: Optional[int] = None
    expected_columns: Optional[List[str]] = None
    max_execution_time_ms: int = Field(5000, description="Performance threshold")
    assertions: List[Assertion] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    setup_sql: Optional[str] = Field(None, description="Setup query before test")
    teardown_sql: Optional[str] = Field(None, description="Cleanup after test")
    skip: bool = False

    @validator("sql")
    def validate_sql(cls, v: Any) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("sql must be a non-empty string")
        return v


class SchemaValidationCase(BaseModel):
    """Schema validation test case."""
    id: str
    name: str
    table_name: str
    expected_columns: List[DatabaseColumn]
    expected_indexes: Optional[List[str]] = None
    expected_constraints: Optional[Dict[str, List[ConstraintType]]] = None
    tags: List[str] = Field(default_factory=list)


class PerformanceAuditCase(BaseModel):
    """Query performance audit test."""
    id: str
    name: str
    query: str
    expected_max_time_ms: int = Field(1000, description="Max acceptable execution time")
    tags: List[str] = Field(default_factory=list)


class SQLTestResult(BaseModel):
    """Result of executing a single SQL test."""
    test_id: str
    test_name: str
    status: TestStatus
    query: str
    rows_returned: int
    rows_affected: int
    execution_time_ms: float
    has_error: bool
    error_message: Optional[str]
    error_code: Optional[str]
    columns_returned: Optional[List[str]]
    sample_data: Optional[List[Dict[str, Any]]] = Field(None, description="First N rows")
    execution_plan: Optional[str] = Field(None, description="EXPLAIN output")
    assertions_passed: int
    assertions_failed: int
    stack_trace: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == TestStatus.PASSED

    @property
    def performance_ok(self) -> bool:
        return self.execution_time_ms <= 5000


class SchemaValidationResult(BaseModel):
    """Result of schema validation."""
    table_name: str
    valid: bool
    columns_valid: bool
    indexes_valid: Optional[bool]
    constraints_valid: Optional[bool]
    actual_columns: List[DatabaseColumn]
    missing_columns: List[str]
    extra_columns: List[str]
    issues: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DatabaseExecutionSummary(BaseModel):
    """Summary of database test execution."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    error_rate: float
    average_execution_time_ms: float
    slow_queries: List[str] = Field(default_factory=list)
    execution_time_seconds: float
    results: List[SQLTestResult]

    @property
    def success_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return (self.passed / self.total_tests) * 100


# ─────────────────────── Configuration Models ───────────────────────


class APIEngineConfig(BaseModel):
    """Configuration for API testing engine."""
    base_url: Optional[str] = None
    timeout: int = Field(30, description="Default timeout for all requests")
    retry_count: int = Field(0, description="Retry failed requests N times")
    retry_delay: int = Field(1, description="Delay between retries in seconds")
    ssl_verify: bool = True
    proxy: Optional[str] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    parallel_execution: bool = False
    max_workers: int = Field(4, description="If parallel_execution=True")


class DatabaseEngineConfig(BaseModel):
    """Configuration for database testing engine."""
    host: str
    port: int = 5432
    database: str
    username: str
    password: str
    ssl: bool = False
    connection_pool_size: int = Field(10)
    timeout: int = Field(30, description="Query timeout in seconds")
    transaction_mode: str = Field("rollback", description="rollback or commit")
    parallel_execution: bool = False
    max_workers: int = Field(4)


# ─────────────────────── Execution Request/Response ───────────────────────


class EngineExecutionRequest(BaseModel):
    """Request to execute tests in an engine."""
    engine_type: str = Field(..., description="'api' or 'database'")
    config: Optional[Dict[str, Any]] = None
    test_cases: List[Dict[str, Any]] = Field(..., description="Serialized test cases")
    tags: Optional[List[str]] = None
    run_id: str = Field(default_factory=lambda: "run_" + datetime.utcnow().isoformat())


class EngineExecutionResponse(BaseModel):
    """Response from engine execution."""
    run_id: str
    engine_type: str
    status: TestStatus
    total_tests: int
    passed: int
    failed: int
    skipped: int
    execution_time_seconds: float
    results: List[Dict[str, Any]]
    error: Optional[str] = None
