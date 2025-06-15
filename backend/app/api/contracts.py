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
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("/", response_model=List[DataContractResponse])
async def get_contracts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all contracts with optional filtering."""
    contracts = ContractService.get_contracts(db=db, skip=skip, limit=limit, search=search, status=status)
    return contracts


@router.get("/{contract_id}", response_model=DataContractResponse)
async def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """Get a specific contract by ID."""
    contract = ContractService.get_contract(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.post("/", response_model=DataContractResponse)
async def create_contract(contract: DataContractCreate, db: Session = Depends(get_db)):
    """Create a new data contract."""
    return ContractService.create_contract(db=db, contract=contract)


@router.put("/{contract_id}", response_model=DataContractResponse)
async def update_contract(
    contract_id: int, contract_update: DataContractUpdate, db: Session = Depends(get_db)
):
    """Update an existing contract."""
    contract = ContractService.update_contract(
        db=db, contract_id=contract_id, contract_update=contract_update
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.delete("/{contract_id}", response_model=MessageResponse)
async def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """Delete a contract."""
    success = ContractService.delete_contract(db=db, contract_id=contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contract not found")
    return MessageResponse(message="Contract deleted successfully")


@router.post("/auto-generate", response_model=List[dict])
async def auto_generate_fields(request: AutoGenerateRequest):
    """Auto-generate contract fields from various sources."""
    try:
        if request.source_type == "database":
            fields = AutoGenerationService.generate_from_database_schema(
                request.source_data, request.table_name or "unknown_table"
            )
        elif request.source_type == "api":
            fields = AutoGenerationService.generate_from_api_response(request.source_data)
        elif request.source_type == "file":
            fields = AutoGenerationService.generate_from_csv_data(request.source_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid source type")

        return [field.dict() for field in fields]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
