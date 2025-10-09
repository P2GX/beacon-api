"""Beacon v2 datasets endpoints."""

from fastapi import APIRouter, HTTPException, Query

from beacon_api.api.dependencies import DatasetServiceDep
from beacon_api.models.entities import Dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("", response_model=list[Dataset])
async def list_datasets(
    service: DatasetServiceDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
) -> list[Dataset]:
    """List all datasets with pagination."""
    try:
        return await service.list(skip=skip, limit=limit)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")


@router.get("/{dataset_id}", response_model=Dataset)
async def get_dataset(
    dataset_id: str,
    service: DatasetServiceDep,
) -> Dataset:
    """Retrieve a specific dataset by ID."""
    try:
        dataset = await service.get_by_id(dataset_id)
        if dataset is None:
            raise HTTPException(status_code=404, detail="Dataset not found")
        return dataset
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Service not implemented")
