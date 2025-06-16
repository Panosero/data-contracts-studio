"""Data contracts API endpoints.

This module provides RESTful API endpoints for managing data contracts,
including CRUD operations and auto-generation capabilities.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.contract import (
    AutoGenerateRequest,
    DataContractCreate,
    DataContractResponse,
    DataContractUpdate,
    MessageResponse,
)
from app.services.auto_generation_service import AutoGenerationService
from app.services.contract_service import ContractService

# Configure logging
logger = logging.getLogger(__name__)

# Router configuration
router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("/", response_model=List[DataContractResponse])
async def get_contracts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    search: Optional[str] = Query(None, description="Search term for contract names"),
    status: Optional[str] = Query(None, description="Filter by contract status"),
    db: Session = Depends(get_db),
) -> List[DataContractResponse]:
    """Retrieve all data contracts with optional filtering and pagination.

    Args:
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        search: Optional search term to filter contract names.
        status: Optional status filter (active, inactive, deprecated).
        db: Database session dependency.

    Returns:
        List[DataContractResponse]: List of data contracts matching criteria.

    Raises:
        HTTPException: If database query fails.
    """
    try:
        contracts = ContractService.get_contracts(
            db=db, skip=skip, limit=limit, search=search, status=status
        )
        logger.info(
            f"Retrieved {len(contracts)} contracts with filters: search={search}, status={status}"
        )
        return contracts
    except Exception as e:
        logger.error(f"Failed to retrieve contracts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve contracts"
        )


@router.get("/{contract_id}", response_model=DataContractResponse)
async def get_contract(contract_id: int, db: Session = Depends(get_db)) -> DataContractResponse:
    """Retrieve a specific data contract by ID.

    Args:
        contract_id: Unique identifier for the contract.
        db: Database session dependency.

    Returns:
        DataContractResponse: The requested data contract.

    Raises:
        HTTPException: If contract not found or database error occurs.
    """
    try:
        contract = ContractService.get_contract(db=db, contract_id=contract_id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract with ID {contract_id} not found",
            )
        logger.info(f"Retrieved contract: {contract.name} v{contract.version}")
        return contract
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve contract {contract_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve contract"
        )


@router.post("/", response_model=DataContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: DataContractCreate, db: Session = Depends(get_db)
) -> DataContractResponse:
    """Create a new data contract.

    Args:
        contract: Contract data for creation.
        db: Database session dependency.

    Returns:
        DataContractResponse: The newly created contract.

    Raises:
        HTTPException: If creation fails or validation errors occur.
    """
    try:
        new_contract = ContractService.create_contract(db=db, contract=contract)
        logger.info(f"Created new contract: {new_contract.name} v{new_contract.version}")
        return new_contract
    except ValueError as e:
        logger.warning(f"Contract creation validation failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create contract: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create contract"
        )


@router.put("/{contract_id}", response_model=DataContractResponse)
async def update_contract(
    contract_id: int, contract_update: DataContractUpdate, db: Session = Depends(get_db)
) -> DataContractResponse:
    """Update an existing data contract.

    Args:
        contract_id: ID of the contract to update.
        contract_update: Updated contract data.
        db: Database session dependency.

    Returns:
        DataContractResponse: The updated contract.

    Raises:
        HTTPException: If contract not found or update fails.
    """
    try:
        updated_contract = ContractService.update_contract(
            db=db, contract_id=contract_id, contract_update=contract_update
        )
        if not updated_contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract with ID {contract_id} not found",
            )
        logger.info(f"Updated contract: {updated_contract.name} v{updated_contract.version}")
        return updated_contract
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update contract {contract_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update contract"
        )


@router.delete("/{contract_id}", response_model=MessageResponse)
async def delete_contract(contract_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    """Delete a data contract.

    Args:
        contract_id: ID of the contract to delete.
        db: Database session dependency.

    Returns:
        MessageResponse: Success confirmation message.

    Raises:
        HTTPException: If contract not found or deletion fails.
    """
    try:
        success = ContractService.delete_contract(db=db, contract_id=contract_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract with ID {contract_id} not found",
            )
        logger.info(f"Deleted contract with ID: {contract_id}")
        return MessageResponse(message="Contract deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete contract {contract_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete contract"
        )


@router.post("/auto-generate", response_model=List[dict])
async def auto_generate_fields(request: AutoGenerateRequest) -> List[dict]:
    """Auto-generate contract fields from various data sources.

    This endpoint analyzes data from different sources (database schemas,
    API responses, or file uploads) and automatically generates field
    definitions for data contracts.

    Args:
        request: Auto-generation request with source type and data.

    Returns:
        List[dict]: Generated field definitions.

    Raises:
        HTTPException: If generation fails or invalid source type.
    """
    try:
        logger.info(f"Auto-generating fields from {request.source_type} source")

        # Generate fields based on source type
        if request.source_type == "database":
            fields = AutoGenerationService.generate_from_database_schema(
                request.source_data, request.table_name or "unknown_table"
            )
        elif request.source_type == "api":
            fields = AutoGenerationService.generate_from_api_response(request.source_data)
        elif request.source_type == "file":
            fields = AutoGenerationService.generate_from_csv_data(request.source_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported source type: {request.source_type}",
            )

        # Convert to dict format for response
        field_dicts = [field.dict() for field in fields]
        logger.info(f"Generated {len(field_dicts)} fields from {request.source_type} source")
        return field_dicts

    except ValueError as e:
        logger.warning(f"Auto-generation validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid source data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Auto-generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to auto-generate fields",
        )
