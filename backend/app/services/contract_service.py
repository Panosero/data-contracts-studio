from app.models.contract import DataContract
from app.schemas.contract import DataContractCreate, DataContractUpdate
from sqlalchemy.orm import Session
from typing import List, Optional


class ContractService:
    """Service for managing data contracts."""

    @staticmethod
    def get_contract(db: Session, contract_id: int) -> Optional[DataContract]:
        """Get a contract by ID."""
        return db.query(DataContract).filter(DataContract.id == contract_id).first()

    @staticmethod
    def get_contracts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[DataContract]:
        """Get contracts with optional filtering."""
        query = db.query(DataContract)

        if search:
            query = query.filter(DataContract.name.contains(search))

        if status:
            query = query.filter(DataContract.status == status)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_contract(db: Session, contract: DataContractCreate) -> DataContract:
        """Create a new contract."""
        db_contract = DataContract(
            name=contract.name,
            version=contract.version,
            status=contract.status,
            fields=[field.dict() for field in contract.fields],
        )
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        return db_contract

    @staticmethod
    def update_contract(
        db: Session, contract_id: int, contract_update: DataContractUpdate
    ) -> Optional[DataContract]:
        """Update an existing contract."""
        db_contract = ContractService.get_contract(db, contract_id)
        if not db_contract:
            return None

        update_data = contract_update.dict(exclude_unset=True)
        if "fields" in update_data:
            update_data["fields"] = [field.dict() for field in contract_update.fields]

        for field, value in update_data.items():
            setattr(db_contract, field, value)

        db.commit()
        db.refresh(db_contract)
        return db_contract

    @staticmethod
    def delete_contract(db: Session, contract_id: int) -> bool:
        """Delete a contract."""
        db_contract = ContractService.get_contract(db, contract_id)
        if not db_contract:
            return False

        db.delete(db_contract)
        db.commit()
        return True
