"""Beacon v2 individuals endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from beacon_api.api.dependencies import IndividualServiceDep
from beacon_api.models.common import Pagination
from beacon_api.models.entities import Individual
from beacon_api.models.request import (
    BeaconRequestBody,
    RequestedGranularity,
)
from beacon_api.models.response import (
    BeaconBooleanResponse,
    BeaconCountResponse,
    BeaconResponseMeta,
    BeaconResultsetsResponse,
    BeaconSummaryResults,
    ResultsetInstance,
)

router = APIRouter(prefix="/individuals", tags=["individuals"])


@router.get("", response_model=list[Individual])
async def list_individuals(
    service: IndividualServiceDep,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        default=10, ge=1, le=100, description="Maximum number of records to return"
    ),
) -> list[Individual]:
    """
    List all individuals with pagination.

    Args:
        service: Individual service dependency
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Individual objects
    """
    try:
        individuals = await service.list(skip=skip, limit=limit)
        return individuals
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Individual service not implemented. Please provide a concrete implementation.",
        )


@router.get("/{individual_id}", response_model=Individual)
async def get_individual(
    individual_id: str,
    service: IndividualServiceDep,
) -> Individual:
    """
    Retrieve a specific individual by ID.

    Args:
        individual_id: Unique identifier for the individual
        service: Individual service dependency

    Returns:
        Individual object

    Raises:
        HTTPException: 404 if individual not found, 501 if service not implemented
    """
    try:
        individual = await service.get_by_id(individual_id)
        if individual is None:
            raise HTTPException(status_code=404, detail="Individual not found")
        return individual
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Individual service not implemented. Please provide a concrete implementation.",
        )


@router.post("", response_model=BeaconResultsetsResponse)
async def query_individuals(
    request_body: BeaconRequestBody,
    service: IndividualServiceDep,
) -> dict[str, Any]:
    """
    Query individuals based on filters.

    Supports different granularities:
    - boolean: Returns only existence of matches
    - count: Returns count of matches
    - record: Returns full records

    Args:
        request_body: Beacon request with query parameters and filters
        service: Individual service dependency

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
            }

        elif granularity == RequestedGranularity.COUNT:
            count = await service.count(request_body)
            summary = BeaconSummaryResults(exists=count > 0, num_total_results=count)
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
            }

        else:  # RECORD
            individuals = await service.query(request_body)
            result_set = ResultsetInstance(
                id="individuals",
                set_type="individual",
                exists=len(individuals) > 0,
                result_count=len(individuals),
                results=[ind.model_dump() for ind in individuals],
            )
            summary = BeaconSummaryResults(
                exists=len(individuals) > 0,
                num_total_results=len(individuals),
            )
            return {
                "meta": meta.model_dump(),
                "response_summary": summary.model_dump(),
                "response": [result_set.model_dump()],
            }

    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Individual service not implemented. Please provide a concrete implementation.",
        )
