"""Auto-generation service for data contracts.

This module provides services for automatically generating data contract fields
from various data sources including database schemas, API responses, and CSV files.
Following PEP 8, PEP 20 (Zen of Python), and PEP 3107 type annotations.
"""

import json
import re
from app.schemas.contract import FieldSchema
from typing import Any, List


class AutoGenerationService:
    """Service for auto-generating contract fields from various data sources.

    This service provides static methods to analyze different data sources
    and automatically generate field definitions for data contracts.
    """

    @staticmethod
    def sanitize_field_name(name: str) -> str:
        """Sanitize field name to make it valid according to schema rules.

        Only replaces truly problematic characters while preserving
        most special characters commonly used in field names.

        Args:
            name: Raw field name from source data.

        Returns:
            str: Sanitized field name that passes validation.
        """
        if not name or not name.strip():
            return "unnamed_field"

        original_name = name.strip()

        # Replace only truly problematic characters
        # Keep most special characters that are commonly used in data field names
        # but replace spaces for better compatibility
        problematic_chars = {
            " ",  # spaces should be replaced with underscores
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

        sanitized = ""
        for char in original_name:
            if char in problematic_chars:
                sanitized += "_"
            else:
                sanitized += char

        # Ensure it starts with letter, underscore, or dollar sign
        if sanitized and not (sanitized[0].isalpha() or sanitized[0] in ["_", "$"]):
            sanitized = "field_" + sanitized

        # Handle special case where sanitized result is just underscore
        if sanitized == "_":
            sanitized = "field_underscore"

        # Ensure it's not too long
        if len(sanitized) > 100:
            sanitized = sanitized[:100]

        # Ensure it's not empty after sanitization
        if not sanitized:
            sanitized = "unnamed_field"

        return sanitized

    @staticmethod
    def generate_from_database_schema(schema_text: str, table_name: str) -> List[FieldSchema]:
        """Generate field definitions from database schema text.

        Args:
            schema_text: The database schema definition (CREATE TABLE statement).
            table_name: Name of the table being analyzed for documentation purposes.

        Returns:
            List[FieldSchema]: List of field definitions extracted from the schema.

        Raises:
            ValueError: If the schema text cannot be parsed.
        """
        fields = []

        # Clean up the schema text
        schema_text = schema_text.strip()

        # Parse CREATE TABLE statement
        lines = schema_text.split("\n")
        in_table_definition = False

        for line in lines:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("--") or line.startswith("#"):
                continue

            # Check if we're entering table definition
            if line.upper().startswith("CREATE TABLE"):
                in_table_definition = True
                continue

            # Skip until we're in table definition
            if not in_table_definition:
                continue

            # Skip structural elements
            if line in ["(", ")", ");"] or line.upper().startswith(
                ("PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT", "INDEX", "KEY", "UNIQUE")
            ):
                continue

            # Check if we've reached the end of table definition
            if line.endswith(");") or line.upper().startswith(("ALTER", "CREATE INDEX", "INSERT")):
                break

            # Try to parse as field definition
            field = AutoGenerationService._parse_sql_field(line, table_name)
            if field:
                fields.append(field)

        return fields

    @staticmethod
    def generate_from_api_response(api_response: str) -> List[FieldSchema]:
        """Generate field definitions from API JSON response.

        Args:
            api_response: JSON string containing the API response data.

        Returns:
            List[FieldSchema]: List of field definitions extracted from the JSON.

        Raises:
            ValueError: If the JSON format is invalid.
        """
        try:
            data = json.loads(api_response)
            return AutoGenerationService._parse_json_structure(data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON format") from exc

    @staticmethod
    def generate_from_csv_data(csv_data: str) -> List[FieldSchema]:
        """Generate field definitions from CSV data or JSON array.

        This method can handle both CSV format and JSON arrays containing objects.
        It automatically detects the format and processes accordingly.

        Args:
            csv_data: CSV data or JSON array as a string.

        Returns:
            List[FieldSchema]: List of field definitions with inferred types.
        """
        data = csv_data.strip()
        if not data:
            return []

        # Try to parse as JSON first
        try:
            json_data = json.loads(data)
            if isinstance(json_data, list) and json_data:
                # Handle JSON array of objects
                return AutoGenerationService.generate_from_api_response(data)
            elif isinstance(json_data, dict):
                # Handle single JSON object
                return AutoGenerationService.generate_from_api_response(data)
        except json.JSONDecodeError:
            # If not JSON, treat as CSV
            pass

        # Process as CSV
        lines = data.split("\n")
        if not lines:
            return []

        # Handle CSV with headers
        headers = [h.strip().strip('"') for h in lines[0].split(",")]
        fields = []

        # Analyze data types from sample rows
        sample_rows = lines[1:6] if len(lines) > 1 else []  # Use up to 5 sample rows

        for i, header in enumerate(headers):
            if not header:  # Skip empty headers
                continue

            # Extract sample values for this column
            sample_values = []
            for row in sample_rows:
                row_values = [val.strip().strip('"') for val in row.split(",")]
                if i < len(row_values):
                    sample_values.append(row_values[i])

            field_type = AutoGenerationService._infer_type_from_samples(sample_values)
            # Sanitize the field name to ensure it's valid
            sanitized_name = AutoGenerationService.sanitize_field_name(header)

            fields.append(
                FieldSchema(
                    name=sanitized_name,
                    type=field_type,
                    required=True,
                    description=f"Field from CSV column: {header}",
                )
            )

        return fields

    @staticmethod
    def _parse_sql_field(line: str, table_name: str) -> FieldSchema:
        """Parse a single SQL field definition line.

        Args:
            line: SQL field definition line to parse.
            table_name: Name of the table for documentation purposes.

        Returns:
            FieldSchema: Parsed field definition or None if line cannot be parsed.
        """
        # Remove trailing comma and clean up
        line = line.rstrip(",").strip()

        # Skip empty lines or non-field lines
        if not line or len(line.split()) < 2:
            return None

        # Extract field name and type - handle various SQL formats
        parts = line.split()
        field_name = parts[0].strip('`"[]')
        field_type_raw = parts[1].upper()

        # Map SQL types to standard types
        type_mapping = {
            "VARCHAR": "string",
            "TEXT": "string",
            "CHAR": "string",
            "CHARACTER": "string",
            "INTEGER": "integer",
            "INT": "integer",
            "BIGINT": "integer",
            "SMALLINT": "integer",
            "TINYINT": "integer",
            "DECIMAL": "number",
            "NUMERIC": "number",
            "FLOAT": "number",
            "DOUBLE": "number",
            "REAL": "number",
            "BOOLEAN": "boolean",
            "BOOL": "boolean",
            "BIT": "boolean",
            "DATE": "date",
            "DATETIME": "datetime",
            "TIMESTAMP": "datetime",
            "TIME": "time",
            "JSON": "object",
            "JSONB": "object",
            "XML": "object",
            "BLOB": "binary",
            "BINARY": "binary",
            "VARBINARY": "binary",
        }

        # Extract base type (remove size specifications like VARCHAR(255))
        base_type = re.split(r"[(\s]", field_type_raw)[0]
        field_type = type_mapping.get(base_type, "string")

        # Check if field is required (not NULL)
        required = "NOT NULL" in line.upper()

        # Check if field is a primary key (automatically required)
        if "PRIMARY KEY" in line.upper():
            required = True

        return FieldSchema(
            name=AutoGenerationService.sanitize_field_name(field_name),
            type=field_type,
            required=required,
            description=f"Generated from SQL field '{field_name}' in table '{table_name}'",
        )

    @staticmethod
    def _parse_json_structure(data: Any, prefix: str = "") -> List[FieldSchema]:
        """Recursively parse JSON structure to extract field definitions.

        Args:
            data: JSON data structure to parse (dict, list, or primitive).
            prefix: Field name prefix for nested structures.

        Returns:
            List[FieldSchema]: List of field definitions extracted from the structure.
        """
        fields = []

        if isinstance(data, dict):
            for key, value in data.items():
                # Sanitize the field name
                sanitized_key = AutoGenerationService.sanitize_field_name(key)
                field_name = f"{prefix}.{sanitized_key}" if prefix else sanitized_key
                field_type = AutoGenerationService._get_json_type(value)

                if isinstance(value, dict):
                    # Nested object - create a field for the object itself
                    fields.append(
                        FieldSchema(
                            name=field_name,
                            type="object",
                            required=True,
                            description=f"Nested object containing {len(value)} fields (original key: {key})",
                        )
                    )
                    # Add nested fields
                    fields.extend(AutoGenerationService._parse_json_structure(value, field_name))
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    # Array of objects - analyze first object
                    fields.append(
                        FieldSchema(
                            name=field_name,
                            type="array",
                            required=True,
                            description=f"Array of objects (original key: {key})",
                        )
                    )
                    # Sanitize the array prefix to avoid problematic characters like [0]
                    array_prefix = f"{field_name}_0"
                    fields.extend(AutoGenerationService._parse_json_structure(value[0], array_prefix))
                else:
                    fields.append(
                        FieldSchema(
                            name=field_name,
                            type=field_type,
                            required=True,
                            description=f"Field of type {field_type} (original key: {key})",
                        )
                    )

        elif isinstance(data, list) and data:
            # Handle top-level arrays
            if isinstance(data[0], dict):
                # Array of objects - merge all fields from all objects to get complete schema
                all_keys = set()
                for item in data:
                    if isinstance(item, dict):
                        all_keys.update(item.keys())

                # Create a merged object representing the schema
                merged_object = {}
                for key in all_keys:
                    # Find the first non-null value for this key to determine type
                    for item in data:
                        if isinstance(item, dict) and key in item and item[key] is not None:
                            merged_object[key] = item[key]
                            break
                    else:
                        # If all values are null, use None
                        merged_object[key] = None

                # Parse the merged object
                fields.extend(AutoGenerationService._parse_json_structure(merged_object, prefix))
            else:
                # Array of primitives - create a single array field
                array_type = AutoGenerationService._get_json_type(data[0])
                fields.append(
                    FieldSchema(
                        name=prefix or "items",
                        type="array",
                        required=True,
                        description=f"Array of {array_type} values",
                    )
                )

        return fields

    @staticmethod
    def _get_json_type(value: Any) -> str:
        """Determine the data type of a JSON value.

        Args:
            value: The JSON value to analyze.

        Returns:
            str: The corresponding data type string.
        """
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif value is None:
            return "null"
        else:
            return "string"

    @staticmethod
    def _infer_type_from_samples(samples: List[str]) -> str:
        """Infer data type from a list of sample string values.

        Analyzes sample values to determine the most appropriate data type.

        Args:
            samples: List of string values to analyze.

        Returns:
            str: The inferred data type (integer, number, boolean, or string).
        """
        if not samples or all(not s for s in samples):
            return "string"

        # Remove empty values for analysis
        non_empty_samples = [s for s in samples if s]

        # Check if all values are integers
        if all(AutoGenerationService._is_integer(s) for s in non_empty_samples):
            return "integer"

        # Check if all values are floats
        if all(AutoGenerationService._is_float(s) for s in non_empty_samples):
            return "number"

        # Check if all values are booleans
        if all(s.lower() in ["true", "false", "1", "0", "yes", "no"] for s in non_empty_samples):
            return "boolean"

        # Default to string
        return "string"

    @staticmethod
    def _is_integer(value: str) -> bool:
        """Check if a string value represents a valid integer.

        Args:
            value: String value to check.

        Returns:
            bool: True if the value can be parsed as an integer.
        """
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_float(value: str) -> bool:
        """Check if a string value represents a valid float.

        Args:
            value: String value to check.

        Returns:
            bool: True if the value can be parsed as a float.
        """
        try:
            float(value)
            return True
        except ValueError:
            return False
