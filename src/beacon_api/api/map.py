"""Beacon map endpoint."""

from fastapi import APIRouter, Request

from beacon_api.core.beacon_catalog import get_map_response
from beacon_api.core.config import get_settings

router = APIRouter(prefix="/map", tags=["map"])


@router.get("")
async def get_map_endpoint(request: Request) -> dict:
    """Return Beacon map information."""
    settings = get_settings()
    meta = {
        "beaconId": settings.beacon_id,
        "apiVersion": settings.api_version,
        "returnedSchemas": [],
    }
    response = get_map_response(str(request.base_url))
    return {"meta": meta, "response": response}
