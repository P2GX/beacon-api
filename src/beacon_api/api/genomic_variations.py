"""Beacon v2 genomic variations endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException

from beacon_api.api.dependencies import GenomicVariationServiceDep
from beacon_api.api.query_params import (
    FilterParam,
    PaginationLimit,
    PaginationSkip,
    create_request_body_from_params,
)
from beacon_api.api.response_utils import (
    build_meta,
    build_received_request_summary,
    build_resultset_response,
    build_summary,
    filters_to_strings,
    schema_for_entity,
)
from beacon_api.models.request import (
    BeaconRequestBody,
    RequestedGranularity,
)
from beacon_api.models.response import BeaconResultsetsResponse

router = APIRouter(prefix="/g_variants", tags=["genomic_variations"])


@router.get("", response_model=BeaconResultsetsResponse)
async def list_variations(
    service: GenomicVariationServiceDep,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 10,
    filters: FilterParam = None,
) -> dict[str, Any]:
    """
    List all variations with pagination and optional filters.

    Args:
        service: GenomicVariation service dependency
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10, max: 100)
        filters: Beacon v2 filters in JSON or comma-separated format (optional)

    Returns:
        BeaconResultsetsResponse with genomic_variation records

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
        variations = await service.query(request_body)

        requested_schemas = schema_for_entity("genomicVariation")
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
        response = build_resultset_response(
            entity_type="genomicVariation",
            results=[v.model_dump() for v in variations],
        )
        summary = build_summary(
            exists=len(variations) > 0,
            num_total_results=len(variations),
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
        requested_schemas = schema_for_entity("genomicVariation")
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
        response = build_resultset_response(entity_type="genomicVariation", results=[])
        summary = build_summary(exists=False, num_total_results=0)
        return {
            "meta": meta.model_dump(by_alias=True, exclude_none=True),
            "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
            "response": response.model_dump(by_alias=True, exclude_none=True),
        }


@router.post("", response_model=BeaconResultsetsResponse)
async def query_genomic_variations(
    request_body: BeaconRequestBody,
    service: GenomicVariationServiceDep,
) -> dict[str, Any]:
    """
    Query genomic variations based on filters.

    Supports different granularities:
    - boolean: Returns only existence of matches
    - count: Returns count of matches
    - record: Returns full records

    Args:
        request_body: Beacon request with query parameters and filters
        service: Genomic variation service dependency

    Returns:
        BeaconResultsetsResponse with results based on requested granularity

    Raises:
        HTTPException: 501 if service not implemented
    """
    try:
        granularity = request_body.meta.requested_granularity
        requested_schemas = schema_for_entity("genomicVariation")
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
            variations = await service.query(request_body)
            response = build_resultset_response(
                entity_type="genomicVariation",
                results=[v.model_dump() for v in variations],
            )
            summary = build_summary(
                exists=len(variations) > 0,
                num_total_results=len(variations),
            )
            return {
                "meta": meta.model_dump(by_alias=True, exclude_none=True),
                "responseSummary": summary.model_dump(by_alias=True, exclude_none=True),
                "response": response.model_dump(by_alias=True, exclude_none=True),
            }
    except NotImplementedError:
        # Return empty but valid response for unimplemented services (beacon-verifier compliance)
        requested_schemas = schema_for_entity("genomicVariation")
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
            response = build_resultset_response(
                entity_type="genomicVariation", results=[]
            )
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
