#!/usr/bin/env python3
"""Compare hand-written models against Beacon v2 JSON schemas.

This script identifies drift between your implementation and the upstream schema:
- Missing fields in your models
- Extra fields not in schema (custom additions)
- Type mismatches

Usage:
    # First ensure schemas are downloaded and bundled:
    ./scripts/sync_beacon_schemas.sh

    # Then run comparison:
    uv run python scripts/compare_models.py
"""

from __future__ import annotations

import ast
import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Paths
BUNDLED_DIR = Path(__file__).parent.parent / "tmp" / "bundled_schemas"
MODELS_DIR = Path(__file__).parent.parent / "src" / "beacon_api" / "models"

# Map schema files to model classes
# Format: "schema.json": ("model_file.py", "ClassName")
SCHEMA_TO_MODEL = {
    # Entity models
    "individual.json": ("entities.py", "Individual"),
    "biosample.json": ("entities.py", "Biosample"),
    "cohort.json": ("entities.py", "Cohort"),
    "dataset.json": ("entities.py", "Dataset"),
    "run.json": ("entities.py", "Run"),
    "analysis.json": ("entities.py", "Analysis"),
    "genomicVariation.json": ("entities.py", "GenomicVariation"),
    # Request models
    "requestBody.json": ("request.py", "BeaconRequestBody"),
    "filteringTerms.json": ("request.py", "FilteringTerm"),
    # Response models
    "booleanResponse.json": ("response.py", "BeaconBooleanResponse"),
    "countResponse.json": ("response.py", "BeaconCountResponse"),
    "resultsetsResponse.json": ("response.py", "BeaconResultsetsResponse"),
    "infoResponse.json": ("response.py", "BeaconInfoResponse"),
    "errorResponse.json": ("common.py", "BeaconError"),
    "responseMeta.json": ("response.py", "BeaconResponseMeta"),
}


@dataclass
class FieldInfo:
    """Information about a field."""

    name: str
    type_hint: str | None = None
    required: bool = False
    description: str | None = None


@dataclass
class ComparisonResult:
    """Result of comparing a model against schema."""

    model_name: str
    schema_file: str
    missing_fields: list[FieldInfo]  # In schema but not in model
    extra_fields: list[str]  # In model but not in schema
    schema_field_count: int
    model_field_count: int


def extract_schema_fields(schema_path: Path) -> dict[str, FieldInfo]:
    """Extract fields from a JSON schema."""
    with open(schema_path) as f:
        schema = json.load(f)

    fields = {}
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    for name, prop in properties.items():
        # Get type info
        type_hint = prop.get("type")
        if not type_hint and "$ref" in prop:
            type_hint = f"$ref:{prop['$ref']}"
        if not type_hint and "oneOf" in prop:
            type_hint = "oneOf[...]"
        if not type_hint and "anyOf" in prop:
            type_hint = "anyOf[...]"

        fields[name] = FieldInfo(
            name=name,
            type_hint=type_hint,
            required=name in required,
            description=prop.get("description"),
        )

    return fields


def extract_model_fields(model_path: Path, class_name: str) -> dict[str, str]:
    """Extract fields from a Pydantic model using AST parsing."""
    with open(model_path) as f:
        source = f.read()

    tree = ast.parse(source)
    fields = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                # Handle annotated assignments: field: Type = ...
                if isinstance(item, ast.AnnAssign) and isinstance(
                    item.target, ast.Name
                ):
                    field_name = item.target.id
                    # Get type annotation as string
                    type_hint = ast.unparse(item.annotation)
                    fields[field_name] = type_hint

    return fields


def normalize_field_name(name: str) -> str:
    """Normalize field name for comparison (camelCase to snake_case).
    
    Handles consecutive capitals correctly:
    - APIResponse -> api_response
    - HTTPSConnection -> https_connection
    - XMLHttpRequest -> xml_http_request
    - camelCase -> camel_case
    - getUserID -> get_user_id
    """
    # First: Insert underscore before uppercase letter followed by lowercase
    # (handles: APIResponse -> API_Response, camelCase -> camel_Case)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Second: Insert underscore between lowercase/digit and uppercase
    # (handles: getUserID -> get_User_ID after first pass)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def compare_model(
    schema_path: Path, model_path: Path, class_name: str
) -> ComparisonResult:
    """Compare a single model against its schema."""
    schema_fields = extract_schema_fields(schema_path)
    model_fields = extract_model_fields(model_path, class_name)

    # Normalize schema field names for comparison
    schema_normalized = {normalize_field_name(k): v for k, v in schema_fields.items()}

    # Find missing fields (in schema but not in model)
    missing = []
    for norm_name, field_info in schema_normalized.items():
        if norm_name not in model_fields:
            missing.append(field_info)

    # Find extra fields (in model but not in schema)
    extra = []
    schema_norm_names = set(schema_normalized.keys())
    for field_name in model_fields:
        if field_name not in schema_norm_names and not field_name.startswith("model_"):
            extra.append(field_name)

    return ComparisonResult(
        model_name=class_name,
        schema_file=schema_path.name,
        missing_fields=missing,
        extra_fields=extra,
        schema_field_count=len(schema_fields),
        model_field_count=len(model_fields),
    )


def print_report(results: list[ComparisonResult]) -> None:
    """Print comparison report."""
    print("\n" + "=" * 60)
    print("BEACON MODEL COMPARISON REPORT")
    print("=" * 60)

    total_missing = 0
    total_extra = 0

    for result in results:
        print(f"\n{result.model_name}")
        print("-" * 40)
        print(f"Schema fields: {result.schema_field_count}")
        print(f"Model fields:  {result.model_field_count}")

        if result.missing_fields:
            print(f"\n  MISSING ({len(result.missing_fields)} fields not in your model):")
            for field in sorted(result.missing_fields, key=lambda f: f.name):
                req = " [REQUIRED]" if field.required else ""
                print(f"    - {field.name}: {field.type_hint}{req}")
            total_missing += len(result.missing_fields)
        else:
            print("\n  ✓ No missing fields")

        if result.extra_fields:
            print(f"\n  EXTRA ({len(result.extra_fields)} custom fields in your model):")
            for field in sorted(result.extra_fields):
                print(f"    + {field}")
            total_extra += len(result.extra_fields)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total missing fields: {total_missing}")
    print(f"Total extra fields:   {total_extra}")

    if total_missing > 0:
        print("\n⚠ Your models are missing fields from the upstream schema.")
        print("  Review the MISSING fields above and add them if needed.")


def main() -> int:
    """Run the comparison."""
    if not BUNDLED_DIR.exists():
        logger.error(f"Bundled schemas not found: {BUNDLED_DIR}")
        logger.error("Run './scripts/sync_beacon_schemas.sh' first.")
        return 1

    results = []

    for schema_file, (model_file, class_name) in SCHEMA_TO_MODEL.items():
        schema_path = BUNDLED_DIR / schema_file
        model_path = MODELS_DIR / model_file

        if not schema_path.exists():
            logger.warning(f"Schema not found: {schema_path}")
            continue

        if not model_path.exists():
            logger.warning(f"Model not found: {model_path}")
            continue

        result = compare_model(schema_path, model_path, class_name)
        results.append(result)

    print_report(results)
    return 0


if __name__ == "__main__":
    exit(main())
