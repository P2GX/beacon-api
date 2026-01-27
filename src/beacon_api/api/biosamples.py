"""Beacon v2 biosamples endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException

from beacon_api.api.dependencies import BiosampleServiceDep
from beacon_api.api.query_params import (
    FilterParam,
    PaginationLimit,
    PaginationSkip,
    create_request_body_from_params,
)
from beacon_api.models.request import (
    BeaconRequestBody,
    RequestedGranularity,
)
from beacon_api.models.response import (
    BeaconResponseMeta,
    BeaconResultsetsResponse,
    BeaconSummaryResults,
    ResultsetInstance,
)

router = APIRouter(prefix="/biosamples", tags=["biosamples"])


@router.get("", response_model=BeaconResultsetsResponse)
async def list_biosamples(
    service: BiosampleServiceDep,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 10,
    filters: FilterParam = None,
) -> dict[str, Any]:
    """
    List all biosamples with pagination and optional filters.

    Supports Beacon v2 filter formats:
    - JSON: ?filters=[{"id":"UBERON:0000178"},{"id":"PATO:0000011","operator":">","value":"P70Y"}]
    - Comma-separated: ?filters=UBERON:0000178,NCIT:C6975

    Args:
        service: Biosample service dependency
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10, max: 100)
        filters: Beacon v2 filters in JSON or comma-separated format (optional)

    Returns:
        BeaconResultsetsResponse with biosample records

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
        biosamples = await service.query(request_body)

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
            id="biosamples",
            set_type="biosample",
            exists=len(biosamples) > 0,
            result_count=len(biosamples),
            results=[bs.model_dump() for bs in biosamples],
        )

        summary = BeaconSummaryResults(
            exists=len(biosamples) > 0,
            num_total_results=len(biosamples),
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
            id="biosamples",
            set_type="biosample",
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


@router.get("/{biosample_id}", response_model=BeaconResultsetsResponse)
async def get_biosample(
    biosample_id: str,
    service: BiosampleServiceDep,
) -> dict[str, Any]:
    """
    Retrieve a specific biosample by ID.

    Args:
        biosample_id: Unique identifier for the biosample
        service: Biosample service dependency

    Returns:
        BeaconResultsetsResponse containing the biosample

    Raises:
        HTTPException: 404 if biosample not found
    """
    try:
        biosample = await service.get_by_id(biosample_id)
        if biosample is None:
            raise HTTPException(status_code=404, detail="Biosample not found")

        meta = BeaconResponseMeta(
            beacon_id="beacon-skeleton",
            api_version="v2.0",
            returned_granularity="record",
            received_request_summary={
                "requested_granularity": "record",
                "filters": [],
                "requested_id": biosample_id,
            },
        )

        result_set = ResultsetInstance(
            id="biosamples",
            set_type="biosample",
            exists=True,
            result_count=1,
            results=[biosample.model_dump()],
        )

        summary = BeaconSummaryResults(exists=True, num_total_results=1)

        return {
            "meta": meta.model_dump(),
            "response_summary": summary.model_dump(),
            "response": [result_set.model_dump()],
            "info": None,
            "beacon_error": None,
        }

    except NotImplementedError:
        # Return 404 for unimplemented services
        raise HTTPException(status_code=404, detail="Biosample not found") from None


@router.post("", response_model=BeaconResultsetsResponse)
async def query_biosamples(
    request_body: BeaconRequestBody,
    service: BiosampleServiceDep,
) -> dict[str, Any]:
    """
    Query biosamples based on filters.

    Supports different granularities:
    - boolean: Returns only existence of matches
    - count: Returns count of matches
    - record: Returns full records

    Args:
        request_body: Beacon request with query parameters and filters
        service: Biosample service dependency

    Returns:
        BeaconResultsetsResponse with results based on requested granularity

    Raises:
        HTTPException: 501 if service not implemented
    """
    try:
        granularity = request_body.meta.requested_granularity

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
            biosamples = await service.query(request_body)
            result_set = ResultsetInstance(
                id="biosamples",
                set_type="biosample",
                exists=len(biosamples) > 0,
                result_count=len(biosamples),
                results=[bs.model_dump() for bs in biosamples],
            )
            summary = BeaconSummaryResults(
                exists=len(biosamples) > 0,
                num_total_results=len(biosamples),
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
                id="biosamples",
                set_type="biosample",
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
