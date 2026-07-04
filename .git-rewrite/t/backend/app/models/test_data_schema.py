"""Pydantic schemas for test data endpoints."""
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class TestDataCreate(BaseModel):
    """Create test data request."""
    name: str
    data: Dict[str, Any]
    description: Optional[str] = None


class TestDataUpdate(BaseModel):
    """Update test data request."""
    name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class TestDataResponse(BaseModel):
    """Test data response."""
    id: int
    project_id: int
    name: str
    description: Optional[str]
    data: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
