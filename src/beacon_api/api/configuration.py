"""Beacon configuration endpoint."""

from fastapi import APIRouter

from beacon_api.core.beacon_catalog import get_configuration
from beacon_api.core.config import get_settings

router = APIRouter(prefix="/configuration", tags=["configuration"])


@router.get("")
async def get_configuration_endpoint() -> dict:
    """Return Beacon configuration information."""
    settings = get_settings()
    meta = {
        "beaconId": settings.beacon_id,
        "apiVersion": settings.api_version,
        "returnedSchemas": [],
    }
    response = get_configuration(settings)
    return {"meta": meta, "response": response}
