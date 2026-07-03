"""Pydantic request/response schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str

    class Config:
        from_attributes = True


# Project Schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    test_framework: str = "playwright"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    test_framework: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    test_framework: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# TestCase Schemas
class TestCaseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    test_code: str
    test_type: str = "e2e"
    tags: List[str] = []


class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    test_code: Optional[str] = None
    tags: Optional[List[str]] = None


class TestCaseResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str]
    test_type: str
    tags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Execution Schemas
class ExecutionRequest(BaseModel):
    test_case_ids: List[int] = []


class ExecutionResponse(BaseModel):
    id: int
    project_id: int
    status: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    duration_seconds: float
    started_at: Optional[datetime]
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True


# Error Response
class ErrorResponse(BaseModel):
    detail: str
    status_code: int
