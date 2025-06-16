"""Pydantic schemas for data contract validation and serialization.

This module defines the request/response schemas for the data contracts API,
providing type safety, validation, and automatic documentation generation.
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict, List, Literal, Optional


class FieldSchema(BaseModel):
    """Schema for a data contract field definition.

    Represents a single field in a data contract with its type,
    constraints, and metadata.

    Attributes:
        name: Field identifier name.
        type: Data type (string, integer, boolean, etc.).
        required: Whether the field is mandatory.
        description: Optional human-readable description.
        constraints: Additional validation rules and constraints.
        default_value: Default value for the field if not provided.
    """

    name: str = Field(..., description="Field name")
    type: Literal[
        "string", "integer", "number", "boolean", "array", "object", 
        "date", "datetime", "time", "binary", "null"
    ] = Field(..., description="Data type")
    required: bool = Field(default=False, description="Whether field is required")
    description: Optional[str] = Field(None, max_length=500, description="Field description")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Validation constraints")
    default_value: Optional[Any] = Field(None, description="Default value for the field")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate field name format.

        Allows most common special characters used in data field names
        while maintaining basic identifier rules for compatibility.

        Args:
            v: Field name to validate.

        Returns:
            str: Validated field name.

        Raises:
            ValueError: If name contains truly problematic characters.
        """
        if not v or not v.strip():
            raise ValueError("Field name cannot be empty or whitespace only")

        # Strip whitespace
        name = v.strip()

        # Check length constraints
        if len(name) > 100:
            raise ValueError("Field name cannot exceed 100 characters")

        # Must start with letter, underscore, dollar sign, or be purely numeric
        if not (name[0].isalpha() or name[0] in ["_", "$"] or name.isdigit()):
            raise ValueError("Field name must start with a letter, underscore, dollar sign, or be purely numeric")

        # Define truly problematic characters that should be rejected
        # Allow most special characters that are commonly used in field names
        # but reject spaces and characters that cause parsing issues
        problematic_chars = {
            " ",  # spaces should be rejected to encourage underscore usage
            "\t",
            "\n",
            "\r",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            '"',
            "'",
            "`",
            "\\",
            "/",
            "|",
            "<",
            ">",
            "=",
            "+",
            "*",
            "%",
            "&",
            "^",
            "~",
            ":",
            ";",
            ",",
        }

        invalid_chars = [c for c in name if c in problematic_chars]
        if invalid_chars:
            raise ValueError(f"Field name contains problematic characters: {', '.join(set(invalid_chars))}")

        return name


class DataContractBase(BaseModel):
    """Base schema for data contracts with common fields.

    This base class contains all the common fields shared between
    create, update, and response schemas to follow DRY principles.

    Attributes:
        name: Contract name (unique identifier).
        version: Semantic version string.
        status: Contract lifecycle status.
        fields: List of field definitions.
    """

    name: str = Field(..., min_length=1, max_length=255, description="Contract name")
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$", description="Semantic version")
    status: Literal["active", "inactive", "deprecated"] = Field(
        default="active", description="Contract status"
    )
    fields: List[FieldSchema] = Field(..., min_items=1, description="Field definitions")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate contract name format.

        Args:
            v: Contract name to validate.

        Returns:
            str: Validated contract name.
        """
        return v.strip()


class DataContractCreate(DataContractBase):
    """Schema for creating a new data contract.

    Inherits all fields from DataContractBase without modifications.
    Used for POST requests to create new contracts.
    """


class DataContractUpdate(BaseModel):
    """Schema for updating an existing data contract.

    All fields are optional to support partial updates.
    Only provided fields will be updated in the database.

    Attributes:
        name: Optional new contract name.
        version: Optional new version.
        status: Optional new status.
        fields: Optional new field definitions.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    version: Optional[str] = Field(None, pattern=r"^\d+\.\d+\.\d+$")
    status: Optional[Literal["active", "inactive", "deprecated"]] = None
    fields: Optional[List[FieldSchema]] = Field(None, min_items=1)


class DataContractResponse(DataContractBase):
    """Schema for data contract API responses.

    Extends the base schema with database-generated fields
    like ID and timestamps for complete contract representation.

    Attributes:
        id: Database primary key.
        created_at: Contract creation timestamp.
        updated_at: Last modification timestamp.
    """

    id: int = Field(..., description="Contract database ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic configuration for ORM integration."""

        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class AutoGenerateRequest(BaseModel):
    """Schema for auto-generation requests.

    Used to generate data contracts from external sources
    like database schemas, API responses, or file uploads.

    Attributes:
        source_type: Type of data source.
        source_data: Raw source data content.
        table_name: Optional table name for database sources.
        endpoint_url: Optional URL for API sources.
    """

    source_type: Literal["database", "api", "file"] = Field(..., description="Source type")
    source_data: str = Field(..., min_length=1, description="Source data content")
    table_name: Optional[str] = Field(None, max_length=100, description="Database table name")
    endpoint_url: Optional[str] = Field(None, description="API endpoint URL")

    @field_validator("source_data")
    @classmethod
    def validate_source_data(cls, v: str) -> str:
        """Validate source data is not empty.

        Args:
            v: Source data to validate.

        Returns:
            str: Validated source data.
        """
        return v.strip()


class MessageResponse(BaseModel):
    """Schema for simple API response messages.

    Used for operations that return status messages
    rather than data objects.

    Attributes:
        message: Response message text.
        status: Operation status indicator.
    """

    message: str = Field(..., description="Response message")
    status: Literal["success", "error", "warning"] = Field(default="success", description="Response status")
