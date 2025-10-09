"""Beacon v2 runs endpoints."""

from fastapi import APIRouter, HTTPException, Query

from beacon_skeleton.api.dependencies import RunServiceDep
from beacon_skeleton.models.entities import Run

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("", response_model=list[Run])
async def list_runs(
    service: RunServiceDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
) -> list[Run]:
    """List all runs with pagination."""
    try:
        return await service.list(skip=skip, limit=limit)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")


@router.get("/{run_id}", response_model=Run)
async def get_run(
    run_id: str,
    service: RunServiceDep,
) -> Run:
    """Retrieve a specific run by ID."""
    try:
        run = await service.get_by_id(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Run not found")
        return run
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")
