"""SQLAlchemy ORM models for QA automation platform."""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from backend.app.database.base import Base


class TestFramework(str, PyEnum):
    """Supported test frameworks."""
    PLAYWRIGHT = "playwright"
    PYTEST = "pytest"
    SELENIUM = "selenium"
    CYPRESS = "cypress"
    CUSTOM = "custom"


class ExecutionStatus(str, PyEnum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class UserRole(str, PyEnum):
    """User roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    TESTER = "tester"
    VIEWER = "viewer"


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.TESTER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    projects = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    audit_logs = relationship("AuditLog", back_populates="user")


class Project(Base):
    """Project model."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    test_framework = Column(Enum(TestFramework), default=TestFramework.PLAYWRIGHT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="projects", foreign_keys=[owner_id])
    test_cases = relationship("TestCase", back_populates="project", cascade="all, delete-orphan")
    executions = relationship("Execution", back_populates="project", cascade="all, delete-orphan")


class TestCase(Base):
    """Test case model."""
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    test_code = Column(Text, nullable=False)
    test_type = Column(String(50), default="e2e", nullable=False)
    tags = Column(JSON, default=list)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    project = relationship("Project", back_populates="test_cases")
    results = relationship("ExecutionResult", back_populates="test_case", cascade="all, delete-orphan")


class Execution(Base):
    """Test execution model."""
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    total_tests = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    duration_seconds = Column(Float, default=0.0)
    started_at = Column(DateTime, index=True)
    ended_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    project = relationship("Project", back_populates="executions")
    results = relationship("ExecutionResult", back_populates="execution", cascade="all, delete-orphan")
    report = relationship("Report", uselist=False, back_populates="execution", cascade="all, delete-orphan")


class ExecutionResult(Base):
    """Individual test result within an execution."""
    __tablename__ = "execution_results"

    id = Column(Integer, primary_key=True)
    execution_id = Column(Integer, ForeignKey("executions.id"), nullable=False, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False, index=True)
    status = Column(Enum(ExecutionStatus), nullable=False)
    duration_seconds = Column(Float, default=0.0)
    error_message = Column(Text)
    stack_trace = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    execution = relationship("Execution", back_populates="results")
    test_case = relationship("TestCase", back_populates="results")


class Report(Base):
    """Test report model."""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    execution_id = Column(Integer, ForeignKey("executions.id"), nullable=False, index=True, unique=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    html_content = Column(Text)
    json_content = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    execution = relationship("Execution", back_populates="report")


class AuditLog(Base):
    """Audit log for tracking user actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = relationship("User", back_populates="audit_logs")
