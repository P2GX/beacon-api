"""Beacon entry types endpoint."""

from fastapi import APIRouter

from beacon_api.core.beacon_catalog import get_entry_types_response
from beacon_api.core.config import get_settings

router = APIRouter(prefix="/entry_types", tags=["entry_types"])


@router.get("")
async def get_entry_types_endpoint() -> dict:
    """Return Beacon entry types information."""
    settings = get_settings()
    meta = {
        "beaconId": settings.beacon_id,
        "apiVersion": settings.api_version,
        "returnedSchemas": [],
    }
    response = get_entry_types_response()
    return {"meta": meta, "response": response}
