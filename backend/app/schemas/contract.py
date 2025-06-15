from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class FieldSchema(BaseModel):
    """Schema for a data contract field."""

    name: str
    type: str
    required: bool = True
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None


class DataContractBase(BaseModel):
    """Base schema for data contracts."""

    name: str = Field(..., min_length=1, max_length=255)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    status: str = Field(default="active", pattern="^(active|inactive|deprecated)$")
    fields: List[FieldSchema]


class DataContractCreate(DataContractBase):
    """Schema for creating a data contract."""

    pass


class DataContractUpdate(BaseModel):
    """Schema for updating a data contract."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    version: Optional[str] = Field(None, pattern=r"^\d+\.\d+\.\d+$")
    status: Optional[str] = Field(None, pattern="^(active|inactive|deprecated)$")
    fields: Optional[List[FieldSchema]] = None


class DataContractResponse(DataContractBase):
    """Schema for data contract responses."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AutoGenerateRequest(BaseModel):
    """Schema for auto-generation requests."""

    source_type: str = Field(..., pattern="^(database|api|file)$")
    source_data: str
    table_name: Optional[str] = None
    endpoint_url: Optional[str] = None


class MessageResponse(BaseModel):
    """Schema for simple message responses."""

    message: str
    status: str = "success"
