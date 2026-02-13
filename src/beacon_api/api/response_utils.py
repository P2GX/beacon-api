"""Helpers for building Beacon v2 compliant responses."""

from __future__ import annotations

from typing import Any

from beacon_api.core.beacon_catalog import get_schema_reference
from beacon_api.core.config import get_settings
from beacon_api.models.common import SchemaReference
from beacon_api.models.response import (
    BeaconCollectionsResponseBody,
    BeaconResponseMeta,
    BeaconResultsetsResponseBody,
    BeaconSummaryResults,
    ResultsetInstance,
)


def build_received_request_summary(
    *,
    requested_granularity: str,
    filters: list[str],
    pagination: dict[str, int],
    requested_schemas: list[SchemaReference],
    include_resultset_responses: str | None = None,
    request_parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the receivedRequestSummary section with required fields."""
    settings = get_settings()
    summary: dict[str, Any] = {
        "apiVersion": settings.api_version,
        "requestedSchemas": [s.model_dump(by_alias=True) for s in requested_schemas],
        "pagination": pagination,
        "requestedGranularity": requested_granularity,
        "filters": filters,
    }
    if include_resultset_responses is not None:
        summary["includeResultsetResponses"] = include_resultset_responses
    if request_parameters is not None:
        summary["requestParameters"] = request_parameters
    return summary


def build_meta(
    *,
    returned_granularity: str,
    received_request_summary: dict[str, Any],
    returned_schemas: list[SchemaReference],
    test_mode: bool = False,
) -> BeaconResponseMeta:
    """Build Beacon response metadata."""
    settings = get_settings()
    return BeaconResponseMeta(
        beacon_id=settings.beacon_id,
        api_version=settings.api_version,
        returned_granularity=returned_granularity,
        received_request_summary=received_request_summary,
        returned_schemas=returned_schemas,
        test_mode=test_mode,
    )


def build_resultset_response(
    *,
    entity_type: str,
    results: list[dict[str, Any]],
) -> BeaconResultsetsResponseBody:
    """Build a resultSets response wrapper for record-level responses."""
    result_set = ResultsetInstance(
        id=entity_type,
        set_type=entity_type,
        exists=len(results) > 0,
        result_count=len(results),
        results=results,
    )
    return BeaconResultsetsResponseBody(result_sets=[result_set])


def build_collections_response(
    *,
    collections: list[dict[str, Any]],
) -> BeaconCollectionsResponseBody:
    """Build a collections response wrapper for collection endpoints (cohorts, datasets)."""
    return BeaconCollectionsResponseBody(collections=collections)


def build_summary(
    exists: bool, num_total_results: int | None = None
) -> BeaconSummaryResults:
    """Build a response summary."""
    return BeaconSummaryResults(exists=exists, num_total_results=num_total_results)


def schema_for_entity(entity_type: str) -> list[SchemaReference]:
    """Return schema list for an entity type."""
    return [get_schema_reference(entity_type)]


def filters_to_strings(filters: list[Any] | None) -> list[str]:
    """Convert filter models to a list of string identifiers."""
    if not filters:
        return []
    filter_strings: list[str] = []
    for f in filters:
        if isinstance(f, dict):
            value = f.get("id")
        else:
            value = getattr(f, "id", None)
        if value:
            filter_strings.append(str(value))
    return filter_strings
