"""Beacon v2 response models."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from beacon_skeleton.models.common import BeaconError, SchemaReference


class BeaconOrganization(BaseModel):
    """Organization information."""

    id: str = Field(..., description="Organization identifier")
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(
        default=None,
        description="Organization description",
    )
    address: Optional[str] = Field(default=None, description="Organization address")
    welcome_url: Optional[str] = Field(
        default=None,
        description="Welcome page URL",
    )
    contact_url: Optional[str] = Field(
        default=None,
        description="Contact information URL",
    )
    logo_url: Optional[str] = Field(default=None, description="Organization logo URL")


class BeaconInformationalResponse(BaseModel):
    """Beacon informational metadata."""

    id: str = Field(..., description="Beacon identifier")
    name: str = Field(..., description="Beacon name")
    api_version: str = Field(..., description="Beacon API version", examples=["v2.0"])
    environment: str = Field(
        ...,
        description="Beacon environment",
        examples=["production", "development", "staging"],
    )
    organization: BeaconOrganization = Field(
        ...,
        description="Organization running this Beacon",
    )
    description: Optional[str] = Field(
        default=None,
        description="Beacon description",
    )
    version: Optional[str] = Field(
        default=None,
        description="Beacon implementation version",
    )
    welcome_url: Optional[str] = Field(
        default=None,
        description="Welcome page URL",
    )
    alternative_url: Optional[str] = Field(
        default=None,
        description="Alternative URL for this Beacon",
    )
    create_date_time: Optional[str] = Field(
        default=None,
        description="Beacon creation date and time",
    )
    update_date_time: Optional[str] = Field(
        default=None,
        description="Beacon last update date and time",
    )


class BeaconInfoResponse(BaseModel):
    """Beacon info endpoint response."""

    meta: dict[str, Any] = Field(
        ...,
        description="Response metadata",
    )
    response: BeaconInformationalResponse = Field(
        ...,
        description="Beacon information",
    )


class BeaconSummaryResults(BaseModel):
    """Summary of Beacon query results."""

    exists: bool = Field(
        ...,
        description="Whether any results were found",
    )
    num_total_results: Optional[int] = Field(
        default=None,
        description="Total number of results",
    )


class ResultsetInstance(BaseModel):
    """Single result instance from a Beacon query."""

    id: str = Field(..., description="Result identifier")
    set_type: str = Field(
        ...,
        description="Type of the result set",
        examples=["dataset", "individual", "biosample"],
    )
    exists: bool = Field(..., description="Whether results exist in this set")
    result_count: Optional[int] = Field(
        default=None,
        description="Number of results in this set",
    )
    results: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="Actual result records",
    )
    info: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional information about the result set",
    )
    results_handover: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="Handover information for accessing full results",
    )


class BeaconResponseMeta(BaseModel):
    """Beacon response metadata."""

    beacon_id: str = Field(..., description="Beacon identifier")
    api_version: str = Field(..., description="Beacon API version")
    returned_granularity: str = Field(
        ...,
        description="Granularity of the returned data",
        examples=["boolean", "count", "record"],
    )
    received_request_summary: dict[str, Any] = Field(
        ...,
        description="Summary of the received request",
    )
    returned_schemas: Optional[list[SchemaReference]] = Field(
        default=None,
        description="Schemas used in the response",
    )


class BeaconBooleanResponse(BaseModel):
    """Boolean response from Beacon query."""

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        description="Summary of query results",
    )
    info: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional information",
    )
    beacon_error: Optional[BeaconError] = Field(
        default=None,
        description="Error information if query failed",
    )


class BeaconCountResponse(BaseModel):
    """Count response from Beacon query."""

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        description="Summary of query results",
    )
    info: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional information",
    )
    beacon_error: Optional[BeaconError] = Field(
        default=None,
        description="Error information if query failed",
    )


class BeaconResultsetsResponse(BaseModel):
    """Full results response from Beacon query."""

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        description="Summary of query results",
    )
    response: Optional[list[ResultsetInstance]] = Field(
        default=None,
        description="Result sets",
    )
    info: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional information",
    )
    beacon_error: Optional[BeaconError] = Field(
        default=None,
        description="Error information if query failed",
    )
