#!/usr/bin/env python3
"""Data migration script to fix invalid field names in existing contracts.

This script identifies and fixes field names that don't comply with the
current validation rules, ensuring backward compatibility while maintaining
data integrity.
"""

import json
import logging
import sqlite3
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sanitize_field_name(name: str) -> str:
    """Sanitize an invalid field name to make it valid.
    
    Args:
        name: Original field name.
        
    Returns:
        str: Sanitized field name.
    """
    if not name or not name.strip():
        return "field_unknown"
        
    original_name = name.strip()
    
    # Replace invalid characters with underscores
    sanitized = ""
    for char in original_name:
        if char.isalnum() or char in ["_", "-"]:
            sanitized += char
        else:
            sanitized += "_"
    
    # Ensure it starts with letter or underscore
    if sanitized and not (sanitized[0].isalpha() or sanitized[0] == "_"):
        sanitized = "field_" + sanitized
    
    # Handle special case where sanitized result is just underscore
    if sanitized == "_":
        sanitized = "field_underscore"
        
    # Ensure it's not too long  
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
        
    # Ensure it's not empty after sanitization
    if not sanitized:
        sanitized = "field_unknown"
        
    return sanitized


def is_valid_field_name(name: str) -> bool:
    """Check if a field name is valid without modification.
    
    Args:
        name: Field name to check.
        
    Returns:
        bool: True if the name is valid as-is.
    """
    if not name or len(name) > 100:
        return False
        
    # Must start with letter or underscore
    if not (name[0].isalpha() or name[0] == "_"):
        return False
        
    # All characters must be alphanumeric, underscore, or hyphen
    return all(c.isalnum() or c in ["_", "-"] for c in name)


def fix_contract_fields(fields_json: str) -> tuple[str, List[str]]:
    """Fix invalid field names in a contract's fields JSON.
    
    Args:
        fields_json: JSON string containing the fields array.
        
    Returns:
        tuple: (fixed_fields_json, list_of_changes)
    """
    try:
        fields = json.loads(fields_json)
        changes = []
        
        for field in fields:
            if "name" in field:
                original_name = field["name"]
                if not is_valid_field_name(original_name):
                    sanitized_name = sanitize_field_name(original_name)
                    field["name"] = sanitized_name
                    changes.append(f"'{original_name}' -> '{sanitized_name}'")
                    logger.info(f"Fixed field name: {original_name} -> {sanitized_name}")
        
        return json.dumps(fields), changes
        
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error(f"Error processing fields JSON: {e}")
        return fields_json, []


def migrate_database(db_path: str = "data_contracts.db") -> None:
    """Migrate the database to fix invalid field names.
    
    Args:
        db_path: Path to the SQLite database file.
    """
    logger.info(f"Starting database migration for {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all contracts with their fields
        cursor.execute("SELECT id, name, version, fields FROM data_contracts")
        contracts = cursor.fetchall()
        
        total_contracts = len(contracts)
        fixed_contracts = 0
        total_changes = 0
        
        logger.info(f"Found {total_contracts} contracts to check")
        
        # Process each contract
        for contract_id, contract_name, version, fields_json in contracts:
            logger.info(f"Checking contract {contract_id}: {contract_name} v{version}")
            
            # Fix the fields
            fixed_fields_json, changes = fix_contract_fields(fields_json)
            
            if changes:
                # Update the contract in database
                cursor.execute(
                    "UPDATE data_contracts SET fields = ? WHERE id = ?",
                    (fixed_fields_json, contract_id)
                )
                
                fixed_contracts += 1
                total_changes += len(changes)
                
                logger.info(f"Fixed contract {contract_id} with {len(changes)} field changes:")
                for change in changes:
                    logger.info(f"  - {change}")
            else:
                logger.info(f"Contract {contract_id} has no invalid field names")
        
        # Commit changes
        conn.commit()
        
        logger.info("Migration completed successfully!")
        logger.info(f"  - Total contracts processed: {total_contracts}")
        logger.info(f"  - Contracts fixed: {fixed_contracts}")
        logger.info(f"  - Total field name changes: {total_changes}")
        
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()


def preview_changes(db_path: str = "data_contracts.db") -> None:
    """Preview what changes would be made without actually applying them.
    
    Args:
        db_path: Path to the SQLite database file.
    """
    logger.info(f"Previewing changes for {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all contracts with their fields
        cursor.execute("SELECT id, name, version, fields FROM data_contracts")
        contracts = cursor.fetchall()
        
        total_contracts = len(contracts)
        would_fix_contracts = 0
        total_would_change = 0
        
        logger.info(f"Found {total_contracts} contracts to preview")
        
        # Process each contract
        for contract_id, contract_name, version, fields_json in contracts:
            logger.info(f"Previewing contract {contract_id}: {contract_name} v{version}")
            
            # Check what would be fixed
            _, changes = fix_contract_fields(fields_json)
            
            if changes:
                would_fix_contracts += 1
                total_would_change += len(changes)
                
                logger.info(f"Would fix contract {contract_id} with {len(changes)} field changes:")
                for change in changes:
                    logger.info(f"  - {change}")
            else:
                logger.info(f"Contract {contract_id} has no invalid field names")
        
        logger.info("Preview completed!")
        logger.info(f"  - Total contracts that would be processed: {total_contracts}")
        logger.info(f"  - Contracts that would be fixed: {would_fix_contracts}")
        logger.info(f"  - Total field name changes that would be made: {total_would_change}")
        
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        # Preview mode
        preview_changes()
    else:
        # Migration mode
        migrate_database()
