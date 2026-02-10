"""Beacon catalog helpers for configuration, entry types, and endpoint maps."""

from __future__ import annotations

from typing import Any

from beacon_api.core.config import Settings
from beacon_api.models.common import SchemaReference

ENTRY_TYPES: dict[str, dict[str, str]] = {
    "individual": {
        "name": "Individual",
        "schema": "tmp/bundled_schemas/individual.json",
        "root_path": "/api/individuals",
        "single_path": "/api/individuals/{id}",
    },
    "biosample": {
        "name": "Biosample",
        "schema": "tmp/bundled_schemas/biosample.json",
        "root_path": "/api/biosamples",
        "single_path": "/api/biosamples/{id}",
    },
    "genomicVariation": {
        "name": "Genomic Variation",
        "schema": "tmp/bundled_schemas/genomicVariation.json",
        "root_path": "/api/g_variants",
        "single_path": "/api/g_variants/{id}",
    },
    "analysis": {
        "name": "Analysis",
        "schema": "tmp/bundled_schemas/analysis.json",
        "root_path": "/api/analyses",
        "single_path": None,
    },
    "cohort": {
        "name": "Cohort",
        "schema": "tmp/bundled_schemas/cohort.json",
        "root_path": "/api/cohorts",
        "single_path": None,
    },
    "dataset": {
        "name": "Dataset",
        "schema": "tmp/bundled_schemas/dataset.json",
        "root_path": "/api/datasets",
        "single_path": None,
    },
    "run": {
        "name": "Run",
        "schema": "tmp/bundled_schemas/run.json",
        "root_path": "/api/runs",
        "single_path": None,
    },
}


def get_schema_reference(entity_type: str) -> SchemaReference:
    """Return the schema reference for an entity type."""
    entry = ENTRY_TYPES[entity_type]
    return SchemaReference(entity_type=entity_type, schema=entry["schema"])


def get_entry_types() -> dict[str, Any]:
    """Return entry type definitions for configuration and entry_types endpoints."""
    entry_types: dict[str, Any] = {}
    for entry_type, entry in ENTRY_TYPES.items():
        entry_types[entry_type] = {
            "id": entry_type,
            "name": entry["name"],
            "partOfSpecification": "Beacon v2.0",
            "description": f"{entry['name']} entry type for Beacon v2",
            "defaultSchema": {
                "id": entry_type,
                "name": entry["name"],
                "referenceToSchemaDefinition": entry["schema"],
                "schemaVersion": "2.0.0",
            },
            "ontologyTermForThisType": {
                "id": f"CUSTOM:{entry_type}",
                "label": entry["name"],
            },
        }
    return entry_types


def get_configuration(settings: Settings) -> dict[str, Any]:
    """Return the Beacon configuration response payload."""
    environment_map = {
        "prod": "PROD",
        "production": "PROD",
        "test": "TEST",
        "staging": "TEST",
        "dev": "DEV",
        "development": "DEV",
    }
    production_status = environment_map.get(settings.environment.lower(), "DEV")

    return {
        "$schema": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2/main/framework/json/configuration/beaconConfigurationSchema.json",
        "maturityAttributes": {
            "productionStatus": production_status,
        },
        "securityAttributes": {
            "defaultGranularity": "record",
            "securityLevels": ["PUBLIC"],
        },
        "entryTypes": get_entry_types(),
    }


def get_entry_types_response() -> dict[str, Any]:
    """Return the entry types response payload."""
    return {
        "entryTypes": get_entry_types(),
    }


def get_map_response(base_url: str) -> dict[str, Any]:
    """Return the map response payload."""
    base_url = base_url.rstrip("/")
    endpoint_sets: dict[str, Any] = {}

    for entry_type, entry in ENTRY_TYPES.items():
        root_url = f"{base_url}{entry['root_path']}"
        single_path = entry.get("single_path")
        endpoint_sets[entry_type] = {
            "entryType": entry_type,
            "rootUrl": root_url,
            "openAPIEndpointsDefinition": f"{base_url}/openapi.json",
        }
        if single_path:
            endpoint_sets[entry_type]["singleEntryUrl"] = f"{base_url}{single_path}"

    return {
        "$schema": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2/main/framework/json/configuration/beaconMapSchema.json",
        "endpointSets": endpoint_sets,
    }
