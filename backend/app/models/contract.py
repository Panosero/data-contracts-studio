from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class DataContract(Base):
    """Data contract model."""

    __tablename__ = "data_contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    version = Column(String, nullable=False)
    status = Column(String, default="active")
    fields = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<DataContract(name='{self.name}', version='{self.version}')>"
