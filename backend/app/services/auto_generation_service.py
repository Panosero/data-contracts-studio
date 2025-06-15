import json
import re
from app.schemas.contract import FieldSchema
from typing import Any, List


class AutoGenerationService:
    """Service for auto-generating contracts from various sources."""

    @staticmethod
    def generate_from_database_schema(schema_text: str, table_name: str) -> List[FieldSchema]:
        """Generate fields from database schema."""
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
            if (line in ["(", ")", ");"] or 
                line.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT", "INDEX", "KEY", "UNIQUE"))):
                continue
                
            # Check if we've reached the end of table definition
            if line.endswith(");") or line.upper().startswith(("ALTER", "CREATE INDEX", "INSERT")):
                break
                
            # Try to parse as field definition
            field = AutoGenerationService._parse_sql_field(line)
            if field:
                fields.append(field)

        return fields

    @staticmethod
    def generate_from_api_response(api_response: str) -> List[FieldSchema]:
        """Generate fields from API JSON response."""
        try:
            data = json.loads(api_response)
            return AutoGenerationService._parse_json_structure(data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON format") from exc

    @staticmethod
    def generate_from_csv_data(csv_data: str) -> List[FieldSchema]:
        """Generate fields from CSV data."""
        lines = csv_data.strip().split("\n")
        if not lines:
            return []

        headers = [h.strip() for h in lines[0].split(",")]
        fields = []

        # Analyze data types from sample rows
        sample_rows = lines[1:6] if len(lines) > 1 else []  # Use up to 5 sample rows

        for i, header in enumerate(headers):
            field_type = AutoGenerationService._infer_type_from_samples(
                [row.split(",")[i].strip() if i < len(row.split(",")) else "" for row in sample_rows]
            )

            fields.append(
                FieldSchema(
                    name=header,
                    type=field_type,
                    required=True,
                    description=f"Field from CSV column: {header}",
                )
            )

        return fields

    @staticmethod
    def _parse_sql_field(line: str) -> FieldSchema:
        """Parse a single SQL field definition."""
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
            name=field_name,
            type=field_type,
            required=required,
            description=f"Generated from SQL field: {field_name}",
        )

    @staticmethod
    def _parse_json_structure(data: Any, prefix: str = "") -> List[FieldSchema]:
        """Recursively parse JSON structure to extract fields."""
        fields = []

        if isinstance(data, dict):
            for key, value in data.items():
                field_name = f"{prefix}.{key}" if prefix else key
                field_type = AutoGenerationService._get_json_type(value)

                if isinstance(value, dict):
                    # Nested object - create a field for the object itself
                    fields.append(
                        FieldSchema(
                            name=field_name,
                            type="object",
                            required=True,
                            description=f"Nested object containing {len(value)} fields",
                        )
                    )
                    # Add nested fields
                    fields.extend(AutoGenerationService._parse_json_structure(value, field_name))
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    # Array of objects - analyze first object
                    fields.append(
                        FieldSchema(
                            name=field_name, type="array", required=True, description="Array of objects"
                        )
                    )
                    fields.extend(AutoGenerationService._parse_json_structure(value[0], f"{field_name}[0]"))
                else:
                    fields.append(
                        FieldSchema(
                            name=field_name,
                            type=field_type,
                            required=True,
                            description=f"Field of type {field_type}",
                        )
                    )

        return fields

    @staticmethod
    def _get_json_type(value: Any) -> str:
        """Determine JSON value type."""
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
        """Infer data type from sample values."""
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
        """Check if a string represents an integer."""
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_float(value: str) -> bool:
        """Check if a string represents a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False
