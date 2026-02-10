"""Beacon v2 cohorts endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException

from beacon_api.api.dependencies import CohortServiceDep
from beacon_api.api.query_params import (
    FilterParam,
    PaginationLimit,
    PaginationSkip,
    create_request_body_from_params,
)
from beacon_api.api.response_utils import (
    build_collections_response,
    build_meta,
    build_received_request_summary,
    build_resultset_response,
    build_summary,
    filters_to_strings,
    schema_for_entity,
)
from beacon_api.models.request import BeaconRequestBody, RequestedGranularity
from beacon_api.models.response import BeaconCollectionsResponse, BeaconResultsetsResponse

router = APIRouter(prefix="/cohorts", tags=["cohorts"])


@router.get("", response_model=BeaconCollectionsResponse)
async def list_cohorts(
    service: CohortServiceDep,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 10,
    filters: FilterParam = None,
) -> dict[str, Any]:
    """
    List all cohorts with pagination and optional filters.

    Args:
        service: Cohort service dependency
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10, max: 100)
        filters: Beacon v2 filters in JSON or comma-separated format (optional)

    Returns:
        BeaconCollectionsResponse with cohort collections

    Raises:
        HTTPException: 400 if filters are invalid
    """
    try:
        request_body = create_request_body_from_params(
            skip=skip,
            limit=limit,
            granularity=RequestedGranularity.RECORD,
            filters=filters,
        )
        cohorts = await service.query(request_body)

        requested_schemas = schema_for_entity("cohort")
        received_request_summary = build_received_request_summary(
            requested_granularity="record",
            filters=filters_to_strings(request_body.filters),
            pagination={"skip": skip, "limit": limit},
            requested_schemas=requested_schemas,
        )
        meta = build_meta(
            returned_granularity="record",
            received_request_summary=received_request_summary,
            returned_schemas=requested_schemas,
        )
        response = build_collections_response(
            collections=[c.model_dump() for c in cohorts],
        )
        summary = build_summary(
            exists=len(cohorts) > 0,
            num_total_results=len(cohorts),
        )

        return {
            "meta": meta.model_dump(by_alias=True, exclude_none=True),
            "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
            "response": response.model_dump(by_alias=True, exclude_none=True),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None
    except NotImplementedError:
        # Return empty but valid response for unimplemented services
        requested_schemas = schema_for_entity("cohort")
        received_request_summary = build_received_request_summary(
            requested_granularity="record",
            filters=[],
            pagination={"skip": skip, "limit": limit},
            requested_schemas=requested_schemas,
        )
        meta = build_meta(
            returned_granularity="record",
            received_request_summary=received_request_summary,
            returned_schemas=requested_schemas,
        )
        response = build_collections_response(collections=[])
        summary = build_summary(exists=False, num_total_results=0)
        return {
            "meta": meta.model_dump(by_alias=True, exclude_none=True),
            "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
            "response": response.model_dump(by_alias=True, exclude_none=True),
        }


@router.post("", response_model=BeaconResultsetsResponse)
async def query_cohorts(
    request_body: BeaconRequestBody,
    service: CohortServiceDep,
) -> dict[str, Any]:
    """
    Query cohorts based on filters.

    Supports different granularities:
    - boolean: Returns only existence of matches
    - count: Returns count of matches
    - record: Returns full records

    Args:
        request_body: Beacon request with query parameters and filters
        service: Cohort service dependency

    Returns:
        BeaconResultsetsResponse with results based on requested granularity

    Raises:
        HTTPException: 501 if service not implemented
    """
    try:
        granularity = request_body.meta.requested_granularity

        # Create response metadata
        requested_schemas = schema_for_entity("cohort")
        received_request_summary = build_received_request_summary(
            requested_granularity=granularity.value,
            filters=filters_to_strings(request_body.filters),
            pagination=request_body.meta.pagination or {"skip": 0, "limit": 0},
            requested_schemas=requested_schemas,
            include_resultset_responses=request_body.meta.include_resultset_responses,
        )
        meta = build_meta(
            returned_granularity=granularity.value,
            received_request_summary=received_request_summary,
            returned_schemas=requested_schemas,
        )

        if granularity == RequestedGranularity.BOOLEAN:
            exists = await service.exists(request_body)
            summary = build_summary(exists=exists)
            return {
                "meta": meta.model_dump(by_alias=True, exclude_none=True),
                "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
            }

        elif granularity == RequestedGranularity.COUNT:
            count = await service.count(request_body)
            summary = build_summary(exists=count > 0, num_total_results=count)
            return {
                "meta": meta.model_dump(by_alias=True, exclude_none=True),
                "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
            }

        else:  # RECORD
            cohorts = await service.query(request_body)
            response = build_resultset_response(
                entity_type="cohort",
                results=[c.model_dump() for c in cohorts],
            )
            summary = build_summary(
                exists=len(cohorts) > 0,
                num_total_results=len(cohorts),
            )
            return {
                "meta": meta.model_dump(by_alias=True, exclude_none=True),
                "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
                "response": response.model_dump(by_alias=True, exclude_none=True),
            }

    except NotImplementedError:
        # Return empty but valid response for unimplemented services (beacon-verifier compliance)
        requested_schemas = schema_for_entity("cohort")
        received_request_summary = build_received_request_summary(
            requested_granularity=request_body.meta.requested_granularity.value,
            filters=filters_to_strings(request_body.filters),
            pagination=request_body.meta.pagination or {"skip": 0, "limit": 0},
            requested_schemas=requested_schemas,
            include_resultset_responses=request_body.meta.include_resultset_responses,
        )
        meta = build_meta(
            returned_granularity=request_body.meta.requested_granularity.value,
            received_request_summary=received_request_summary,
            returned_schemas=requested_schemas,
        )
        summary = build_summary(exists=False, num_total_results=0)

        if request_body.meta.requested_granularity == RequestedGranularity.RECORD:
            response = build_resultset_response(entity_type="cohort", results=[])
            return {
                "meta": meta.model_dump(by_alias=True, exclude_none=True),
                "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
                "response": response.model_dump(by_alias=True, exclude_none=True),
            }
        else:
            return {
                "meta": meta.model_dump(by_alias=True, exclude_none=True),
                "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
            }
