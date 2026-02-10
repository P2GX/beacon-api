"""Beacon v2 response models."""

from typing import Any

from pydantic import BaseModel, Field

from beacon_api.models.common import BeaconError, SchemaReference
from beacon_api.models.common_types import OntologyTerm


class BeaconOrganization(BaseModel):
    """Organization information."""

    id: str = Field(..., description="Organization identifier")
    name: str = Field(..., description="Organization name")
    description: str | None = Field(
        default=None,
        description="Organization description",
    )
    address: str | None = Field(default=None, description="Organization address")
    welcome_url: str | None = Field(
        default=None,
        description="Welcome page URL",
    )
    contact_url: str | None = Field(
        default=None,
        description="Contact information URL",
    )
    logo_url: str | None = Field(default=None, description="Organization logo URL")


class BeaconInformationalResponse(BaseModel):
    """Beacon informational metadata."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Beacon identifier")
    name: str = Field(..., description="Beacon name")
    api_version: str = Field(
        ...,
        alias="apiVersion",
        description="Beacon API version",
        examples=["v2.0"],
    )
    environment: str = Field(
        ...,
        description="Beacon environment",
        examples=["prod", "test", "dev", "staging"],
    )
    organization: BeaconOrganization = Field(
        ...,
        description="Organization running this Beacon",
    )
    description: str | None = Field(
        default=None,
        description="Beacon description",
    )
    version: str | None = Field(
        default=None,
        description="Beacon implementation version",
    )
    welcome_url: str | None = Field(
        default=None,
        alias="welcomeUrl",
        description="Welcome page URL",
    )
    alternative_url: str | None = Field(
        default=None,
        alias="alternativeUrl",
        description="Alternative URL for this Beacon",
    )
    create_date_time: str | None = Field(
        default=None,
        alias="createDateTime",
        description="Beacon creation date and time",
    )
    update_date_time: str | None = Field(
        default=None,
        alias="updateDateTime",
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
    num_total_results: int | None = Field(
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
    result_count: int | None = Field(
        default=None,
        description="Number of results in this set",
    )
    results: list[dict[str, Any]] | None = Field(
        default=None,
        description="Actual result records",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information about the result set",
    )
    results_handover: list[dict[str, Any]] | None = Field(
        default=None,
        description="Handover information for accessing full results",
    )


class BeaconResponseMeta(BaseModel):
    """Beacon response metadata."""

    model_config = {"populate_by_name": True}

    beacon_id: str = Field(..., alias="beaconId", description="Beacon identifier")
    api_version: str = Field(..., alias="apiVersion", description="Beacon API version")
    returned_granularity: str = Field(
        ...,
        alias="returnedGranularity",
        description="Granularity of the returned data",
        examples=["boolean", "count", "record"],
    )
    received_request_summary: dict[str, Any] = Field(
        ...,
        alias="receivedRequestSummary",
        description="Summary of the received request",
    )
    returned_schemas: list[SchemaReference] | None = Field(
        default=None,
        alias="returnedSchemas",
        description="Schemas used in the response",
    )
    test_mode: bool | None = Field(
        default=None,
        alias="testMode",
        description="Indicates if the request was executed in test mode",
    )


class BeaconHandover(BaseModel):
    """Handover for linking to external data sources."""

    model_config = {"populate_by_name": True}

    handover_type: OntologyTerm = Field(
        ...,
        alias="handoverType",
        description="Handover type (ontology term)",
    )
    url: str = Field(..., description="URL to access the data")
    note: str | None = Field(default=None, description="Additional note")


class BeaconBooleanResponse(BaseModel):
    """Boolean response from Beacon query."""

    model_config = {"populate_by_name": True}

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        alias="responseSummary",
        description="Summary of query results",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] | None = Field(
        default=None,
        alias="beaconHandovers",
        description="Handovers for accessing data externally",
    )
    beacon_error: BeaconError | None = Field(
        default=None,
        alias="beaconError",
        description="Error information if query failed",
    )


class BeaconCountResponse(BaseModel):
    """Count response from Beacon query."""

    model_config = {"populate_by_name": True}

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        alias="responseSummary",
        description="Summary of query results",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] | None = Field(
        default=None,
        alias="beaconHandovers",
        description="Handovers for accessing data externally",
    )
    beacon_error: BeaconError | None = Field(
        default=None,
        alias="beaconError",
        description="Error information if query failed",
    )


class BeaconResultsetsResponse(BaseModel):
    """Full results response from Beacon query."""

    model_config = {"populate_by_name": True}

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        alias="responseSummary",
        description="Summary of query results",
    )
    response: list[ResultsetInstance] | None = Field(
        default=None,
        description="Result sets",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] | None = Field(
        default=None,
        alias="beaconHandovers",
        description="Handovers for accessing data externally",
    )
    beacon_error: BeaconError | None = Field(
        default=None,
        alias="beaconError",
        description="Error information if query failed",
    )
