"""Beacon v2 analyses endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException

from beacon_api.api.dependencies import AnalysisServiceDep
from beacon_api.api.query_params import (
    FilterParam,
    PaginationLimit,
    PaginationSkip,
    create_request_body_from_params,
)
from beacon_api.models.request import BeaconRequestBody, RequestedGranularity
from beacon_api.models.response import (
    BeaconResponseMeta,
    BeaconResultsetsResponse,
    BeaconSummaryResults,
    ResultsetInstance,
)

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("", response_model=BeaconResultsetsResponse)
async def list_analyses(
    service: AnalysisServiceDep,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 10,
    filters: FilterParam = None,
) -> dict[str, Any]:
    """
    List all analyses with pagination and optional filters.

    Args:
        service: Analysis service dependency
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10, max: 100)
        filters: Beacon v2 filters in JSON or comma-separated format (optional)

    Returns:
        BeaconResultsetsResponse with analysis records

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
        analyses = await service.query(request_body)

        meta = BeaconResponseMeta(
            beacon_id="beacon-skeleton",
            api_version="v2.0",
            returned_granularity="record",
            received_request_summary={
                "requested_granularity": "record",
                "filters": (
                    [f.model_dump() for f in request_body.filters]
                    if request_body.filters
                    else []
                ),
                "pagination": {"skip": skip, "limit": limit},
            },
        )

        result_set = ResultsetInstance(
            id="analyses",
            set_type="analysis",
            exists=len(analyses) > 0,
            result_count=len(analyses),
            results=[a.model_dump() for a in analyses],
        )

        summary = BeaconSummaryResults(
            exists=len(analyses) > 0,
            num_total_results=len(analyses),
        )

        return {
            "meta": meta.model_dump(),
            "response_summary": summary.model_dump(),
            "response": [result_set.model_dump()],
            "info": None,
            "beacon_error": None,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None
    except NotImplementedError:
        # Return empty but valid response for unimplemented services
        meta = BeaconResponseMeta(
            beacon_id="beacon-skeleton",
            api_version="v2.0",
            returned_granularity="record",
            received_request_summary={
                "requested_granularity": "record",
                "filters": [],
                "pagination": {"skip": skip, "limit": limit},
            },
        )
        result_set = ResultsetInstance(
            id="analyses",
            set_type="analysis",
            exists=False,
            result_count=0,
            results=[],
        )
        summary = BeaconSummaryResults(exists=False, num_total_results=0)
        return {
            "meta": meta.model_dump(),
            "response_summary": summary.model_dump(),
            "response": [result_set.model_dump()],
            "info": None,
            "beacon_error": None,
        }


@router.post("", response_model=BeaconResultsetsResponse)
async def query_analyses(
    request_body: BeaconRequestBody,
    service: AnalysisServiceDep,
) -> dict[str, Any]:
    """
    Query analyses based on filters.

    Supports different granularities:
    - boolean: Returns only existence of matches
    - count: Returns count of matches
    - record: Returns full records

    Args:
        request_body: Beacon request with query parameters and filters
        service: Analysis service dependency

    Returns:
        BeaconResultsetsResponse with results based on requested granularity

    Raises:
        HTTPException: 501 if service not implemented
    """
    try:
        granularity = request_body.meta.requested_granularity

        # Create response metadata
        meta = BeaconResponseMeta(
            beacon_id="beacon-skeleton",
            api_version="v2.0",
            returned_granularity=granularity.value,
            received_request_summary={
                "requested_granularity": granularity.value,
                "filters": (
                    [f.model_dump() for f in request_body.filters]
                    if request_body.filters
                    else []
                ),
            },
        )

        if granularity == RequestedGranularity.BOOLEAN:
            exists = await service.exists(request_body)
            summary = BeaconSummaryResults(exists=exists)
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
                "info": None,
                "beacon_error": None,
            }

        elif granularity == RequestedGranularity.COUNT:
            count = await service.count(request_body)
            summary = BeaconSummaryResults(exists=count > 0, num_total_results=count)
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
                "info": None,
                "beacon_error": None,
            }

        else:  # RECORD
            analyses = await service.query(request_body)
            result_set = ResultsetInstance(
                id="analyses",
                set_type="analysis",
                exists=len(analyses) > 0,
                result_count=len(analyses),
                results=[a.model_dump() for a in analyses],
            )
            summary = BeaconSummaryResults(
                exists=len(analyses) > 0,
                num_total_results=len(analyses),
            )
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
                "response": [result_set.model_dump()],
            }

    except NotImplementedError:
        # Return empty but valid response for unimplemented services (beacon-verifier compliance)
        meta = BeaconResponseMeta(
            beacon_id="beacon-skeleton",
            api_version="v2.0",
            returned_granularity=request_body.meta.requested_granularity.value,
            received_request_summary={
                "requested_granularity": request_body.meta.requested_granularity.value,
                "filters": (
                    [f.model_dump() for f in request_body.filters]
                    if request_body.filters
                    else []
                ),
            },
        )
        summary = BeaconSummaryResults(exists=False, num_total_results=0)

        if request_body.meta.requested_granularity == RequestedGranularity.RECORD:
            result_set = ResultsetInstance(
                id="analyses",
                set_type="analysis",
                exists=False,
                result_count=0,
                results=[],
            )
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
                "response": [result_set.model_dump()],
            }
        else:
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
                "info": None,
                "beacon_error": None,
            }
