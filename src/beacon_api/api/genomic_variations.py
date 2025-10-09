"""Beacon v2 genomic variations endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from beacon_api.api.dependencies import GenomicVariationServiceDep
from beacon_api.models.entities import GenomicVariation
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

router = APIRouter(prefix="/g_variants", tags=["genomic_variations"])


@router.get("", response_model=list[GenomicVariation])
async def list_genomic_variations(
    service: GenomicVariationServiceDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
) -> list[GenomicVariation]:
    """List all genomic variations with pagination."""
    try:
        return await service.list(skip=skip, limit=limit)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")


@router.get("/{variation_id}", response_model=GenomicVariation)
async def get_genomic_variation(
    variation_id: str,
    service: GenomicVariationServiceDep,
) -> GenomicVariation:
    """Retrieve a specific genomic variation by ID."""
    try:
        variation = await service.get_by_id(variation_id)
        if variation is None:
            raise HTTPException(status_code=404, detail="Genomic variation not found")
        return variation
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")


@router.post("", response_model=BeaconResultsetsResponse)
async def query_genomic_variations(
    request_body: BeaconRequestBody,
    service: GenomicVariationServiceDep,
) -> dict[str, Any]:
    """Query genomic variations based on filters."""
    try:
        granularity = request_body.meta.requested_granularity
        meta = BeaconResponseMeta(
            beacon_id="beacon-skeleton",
            api_version="v2.0",
            returned_granularity=granularity.value,
            received_request_summary={"requested_granularity": granularity.value},
        )

        if granularity == RequestedGranularity.BOOLEAN:
            exists = await service.exists(request_body)
            return {
                "meta": meta.model_dump(),
                "response_summary": BeaconSummaryResults(exists=exists).model_dump(),
            }
        elif granularity == RequestedGranularity.COUNT:
            count = await service.count(request_body)
            return {
                "meta": meta.model_dump(),
                "response_summary": BeaconSummaryResults(
                    exists=count > 0, num_total_results=count
                ).model_dump(),
            }
        else:
            variations = await service.query(request_body)
            return {
                "meta": meta.model_dump(),
                "response_summary": BeaconSummaryResults(
                    exists=len(variations) > 0, num_total_results=len(variations)
                ).model_dump(),
                "response": [
                    ResultsetInstance(
                        id="g_variants",
                        set_type="genomic_variation",
                        exists=len(variations) > 0,
                        result_count=len(variations),
                        results=[v.model_dump() for v in variations],
                    ).model_dump()
                ],
            }
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")
