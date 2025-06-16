"""Data contract model definition.

This module defines the SQLAlchemy model for data contracts, representing
the core entity for schema definitions and contract management.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class DataContract(Base):
    """Data contract model for storing schema definitions.

    This model represents a data contract which defines the structure,
    validation rules, and metadata for data schemas. Each contract
    can have multiple versions and different statuses.

    Attributes:
        id: Primary key identifier.
        name: Human-readable contract name.
        version: Semantic version string (e.g., "1.0.0").
        status: Contract status ("active", "deprecated", "draft").
        fields: JSON field containing the schema definition.
        created_at: Timestamp when the contract was created.
        updated_at: Timestamp when the contract was last modified.
    """

    __tablename__ = "data_contracts"

    # Primary key
    id: int = Column(Integer, primary_key=True, index=True)

    # Contract metadata
    name: str = Column(String, index=True, nullable=False)
    version: str = Column(String, nullable=False)
    status: str = Column(String, default="active")

    # Schema definition
    fields: Dict[str, Any] = Column(JSON, nullable=False)

    # Timestamps
    created_at: Optional[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Optional[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        """String representation of the data contract.

        Returns:
            str: Human-readable representation of the contract.
        """
        return f"<DataContract(id={self.id}, name='{self.name}', version='{self.version}')>"

    def __str__(self) -> str:
        """User-friendly string representation.

        Returns:
            str: User-friendly name and version.
        """
        return f"{self.name} v{self.version}"
