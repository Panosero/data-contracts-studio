"""Contract service module for business logic operations.

This module provides the business logic layer for data contract operations,
implementing the service pattern to separate concerns from API endpoints.
"""

import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.contract import DataContract
from app.schemas.contract import DataContractCreate, DataContractUpdate

# Configure logging
logger = logging.getLogger(__name__)


class ContractService:
    """Service class for data contract business logic operations.

    This class encapsulates all business logic related to data contracts,
    providing a clean interface between API endpoints and database operations.
    Follows the Single Responsibility Principle by focusing solely on
    contract-related business logic.
    """

    @staticmethod
    def get_contract(db: Session, contract_id: int) -> Optional[DataContract]:
        """Retrieve a single data contract by its ID.

        Args:
            db: Database session for executing queries.
            contract_id: Unique identifier for the contract.

        Returns:
            Optional[DataContract]: The contract if found, None otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            contract = db.query(DataContract).filter(DataContract.id == contract_id).first()
            if contract:
                logger.debug(f"Retrieved contract: {contract.name} v{contract.version}")
            else:
                logger.debug(f"Contract with ID {contract_id} not found")
            return contract
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving contract {contract_id}: {str(e)}")
            raise

    @staticmethod
    def get_contracts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[DataContract]:
        """Retrieve multiple data contracts with optional filtering.

        Args:
            db: Database session for executing queries.
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.
            search: Optional search term for contract names.
            status: Optional status filter.

        Returns:
            List[DataContract]: List of contracts matching the criteria.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            query = db.query(DataContract)

            # Apply search filter if provided
            if search:
                search_term = f"%{search.strip()}%"
                query = query.filter(DataContract.name.ilike(search_term))
                logger.debug(f"Applied search filter: {search}")

            # Apply status filter if provided
            if status:
                query = query.filter(DataContract.status == status.strip())
                logger.debug(f"Applied status filter: {status}")

            # Apply pagination
            contracts = query.offset(skip).limit(limit).all()
            logger.info(f"Retrieved {len(contracts)} contracts (skip={skip}, limit={limit})")
            return contracts
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving contracts: {str(e)}")
            raise

    @staticmethod
    def create_contract(db: Session, contract: DataContractCreate) -> DataContract:
        """Create a new data contract.

        Args:
            db: Database session for executing queries.
            contract: Contract data for creation.

        Returns:
            DataContract: The newly created contract.

        Raises:
            ValueError: If contract data is invalid.
            SQLAlchemyError: If database operation fails.
        """
        try:
            # Validate contract name uniqueness
            existing = (
                db.query(DataContract)
                .filter(
                    DataContract.name == contract.name, DataContract.version == contract.version
                )
                .first()
            )

            if existing:
                raise ValueError(
                    f"Contract '{contract.name}' version '{contract.version}' already exists"
                )

            # Create new contract instance
            db_contract = DataContract(
                name=contract.name.strip(),
                version=contract.version.strip(),
                status=contract.status,
                fields=[field.dict() for field in contract.fields],
            )

            # Persist to database
            db.add(db_contract)
            db.commit()
            db.refresh(db_contract)

            logger.info(f"Created contract: {db_contract.name} v{db_contract.version}")
            return db_contract
        except ValueError:
            db.rollback()
            raise
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating contract: {str(e)}")
            raise

    @staticmethod
    def update_contract(
        db: Session, contract_id: int, contract_update: DataContractUpdate
    ) -> Optional[DataContract]:
        """Update an existing data contract.

        Args:
            db: Database session for executing queries.
            contract_id: ID of the contract to update.
            contract_update: Updated contract data.

        Returns:
            Optional[DataContract]: Updated contract if found, None otherwise.

        Raises:
            ValueError: If update data is invalid.
            SQLAlchemyError: If database operation fails.
        """
        try:
            # Retrieve existing contract
            db_contract = ContractService.get_contract(db, contract_id)
            if not db_contract:
                logger.warning(f"Cannot update non-existent contract with ID {contract_id}")
                return None

            # Prepare update data, excluding unset fields
            update_data = contract_update.dict(exclude_unset=True)

            # Handle fields conversion if present
            if "fields" in update_data and contract_update.fields:
                update_data["fields"] = [field.dict() for field in contract_update.fields]

            # Validate name/version uniqueness if they're being updated
            if "name" in update_data or "version" in update_data:
                new_name = update_data.get("name", db_contract.name)
                new_version = update_data.get("version", db_contract.version)

                existing = (
                    db.query(DataContract)
                    .filter(
                        DataContract.name == new_name,
                        DataContract.version == new_version,
                        DataContract.id != contract_id,
                    )
                    .first()
                )

                if existing:
                    raise ValueError(
                        f"Contract '{new_name}' version '{new_version}' already exists"
                    )

            # Apply updates to contract
            for field, value in update_data.items():
                if hasattr(db_contract, field):
                    setattr(db_contract, field, value.strip() if isinstance(value, str) else value)

            # Persist changes
            db.commit()
            db.refresh(db_contract)

            logger.info(f"Updated contract: {db_contract.name} v{db_contract.version}")
            return db_contract
        except ValueError:
            db.rollback()
            raise
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error updating contract {contract_id}: {str(e)}")
            raise

    @staticmethod
    def delete_contract(db: Session, contract_id: int) -> bool:
        """Delete a data contract.

        Args:
            db: Database session for executing queries.
            contract_id: ID of the contract to delete.

        Returns:
            bool: True if contract was deleted, False if not found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            # Retrieve contract to delete
            db_contract = ContractService.get_contract(db, contract_id)
            if not db_contract:
                logger.warning(f"Cannot delete non-existent contract with ID {contract_id}")
                return False

            # Delete contract
            db.delete(db_contract)
            db.commit()

            logger.info(f"Deleted contract: {db_contract.name} v{db_contract.version}")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error deleting contract {contract_id}: {str(e)}")
            raise
