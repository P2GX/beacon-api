"""Beacon v2 cohorts endpoints."""

from fastapi import APIRouter, HTTPException, Query

from beacon_skeleton.api.dependencies import CohortServiceDep
from beacon_skeleton.models.entities import Cohort

router = APIRouter(prefix="/cohorts", tags=["cohorts"])


@router.get("", response_model=list[Cohort])
async def list_cohorts(
    service: CohortServiceDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
) -> list[Cohort]:
    """List all cohorts with pagination."""
    try:
        return await service.list(skip=skip, limit=limit)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")


@router.get("/{cohort_id}", response_model=Cohort)
async def get_cohort(
    cohort_id: str,
    service: CohortServiceDep,
) -> Cohort:
    """Retrieve a specific cohort by ID."""
    try:
        cohort = await service.get_by_id(cohort_id)
        if cohort is None:
            raise HTTPException(status_code=404, detail="Cohort not found")
        return cohort
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")
