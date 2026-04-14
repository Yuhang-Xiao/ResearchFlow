"""Small schema helper types."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SchemaField:
    """Minimal field descriptor for future schema inventories."""

    name: str
    dtype: str
    nullable: bool = True
    description: str = ""


def describe_fields(fields: list[SchemaField]) -> list[dict[str, str | bool]]:
    """Convert schema fields to a serializable representation."""

    return [
        {
            "name": field.name,
            "dtype": field.dtype,
            "nullable": field.nullable,
            "description": field.description,
        }
        for field in fields
    ]
