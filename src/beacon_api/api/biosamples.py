"""Beacon v2 biosamples endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from beacon_api.api.dependencies import BiosampleServiceDep
from beacon_api.models.entities import Biosample
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


@router.get("", response_model=list[Biosample])
async def list_biosamples(
    service: BiosampleServiceDep,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        default=10, ge=1, le=100, description="Maximum number of records to return"
    ),
) -> list[Biosample]:
    """
    List all biosamples with pagination.

    Args:
        service: Biosample service dependency
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Biosample objects
    """
    try:
        biosamples = await service.list(skip=skip, limit=limit)
        return biosamples
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Biosample service not implemented. Please provide a concrete implementation.",
        )


@router.get("/{biosample_id}", response_model=Biosample)
async def get_biosample(
    biosample_id: str,
    service: BiosampleServiceDep,
) -> Biosample:
    """
    Retrieve a specific biosample by ID.

    Args:
        biosample_id: Unique identifier for the biosample
        service: Biosample service dependency

    Returns:
        Biosample object

    Raises:
        HTTPException: 404 if biosample not found, 501 if service not implemented
    """
    try:
        biosample = await service.get_by_id(biosample_id)
        if biosample is None:
            raise HTTPException(status_code=404, detail="Biosample not found")
        return biosample
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Biosample service not implemented. Please provide a concrete implementation.",
        )


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
            }

        elif granularity == RequestedGranularity.COUNT:
            count = await service.count(request_body)
            summary = BeaconSummaryResults(exists=count > 0, num_total_results=count)
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
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
        raise HTTPException(
            status_code=501,
            detail="Biosample service not implemented. Please provide a concrete implementation.",
        )
