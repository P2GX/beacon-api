"""Beacon v2 info endpoint.

Provides information about the Beacon service.
"""

from typing import Any

from fastapi import APIRouter

from beacon_api.core.config import get_settings
from beacon_api.models.response import (
    BeaconInfoResponse,
    BeaconInformationalResponse,
    BeaconOrganization,
)

router = APIRouter(prefix="/info", tags=["info"])


@router.get("", response_model=BeaconInfoResponse)
async def get_beacon_info() -> dict[str, Any]:
    """
    Get Beacon service information.

    Returns general information about this Beacon implementation including:
    - Beacon ID and name
    - API version
    - Organization details
    - Available endpoints

    Returns:
        BeaconInfoResponse containing Beacon metadata
    """
    settings = get_settings()

    organization = BeaconOrganization(
        id=settings.organization_id,
        name=settings.organization_name,
        description=settings.organization_description,
        address=settings.organization_address,
        welcome_url=settings.organization_welcome_url,
        contact_url=settings.organization_contact_url,
        logo_url=settings.organization_logo_url,
    )

    response = BeaconInformationalResponse(
        id=settings.beacon_id,
        name=settings.beacon_name,
        api_version=settings.api_version,
        environment=settings.environment,
        organization=organization,
        description=settings.beacon_description,
        version=settings.beacon_version,
        welcome_url=settings.beacon_welcome_url,
        alternative_url=settings.beacon_alternative_url,
        create_date_time=settings.beacon_create_date_time,
        update_date_time=settings.beacon_update_date_time,
    )

    meta = {
        "beaconId": settings.beacon_id,
        "apiVersion": settings.api_version,
        "returnedSchemas": [],
    }

    return {"meta": meta, "response": response.model_dump(by_alias=True)}
