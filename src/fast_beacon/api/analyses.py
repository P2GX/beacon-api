"""Beacon v2 analyses endpoints."""

from fastapi import APIRouter, HTTPException, Query

from fast_beacon.api.dependencies import AnalysisServiceDep
from fast_beacon.models.entities import Analysis

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("", response_model=list[Analysis])
async def list_analyses(
    service: AnalysisServiceDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
) -> list[Analysis]:
    """List all analyses with pagination."""
    try:
        return await service.list(skip=skip, limit=limit)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")


@router.get("/{analysis_id}", response_model=Analysis)
async def get_analysis(
    analysis_id: str,
    service: AnalysisServiceDep,
) -> Analysis:
    """Retrieve a specific analysis by ID."""
    try:
        analysis = await service.get_by_id(analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return analysis
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")
