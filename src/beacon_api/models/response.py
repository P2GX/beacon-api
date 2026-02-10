"""Beacon v2 response models."""

from typing import Any

from pydantic import BaseModel, Field

from beacon_api.models.common import BeaconError, SchemaReference
from beacon_api.models.common_types import OntologyTerm


class BeaconOrganization(BaseModel):
    """Organization information."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Organization identifier")
    name: str = Field(..., description="Organization name")
    description: str | None = Field(
        default=None,
        description="Organization description",
    )
    address: str | None = Field(default=None, description="Organization address")
    welcome_url: str | None = Field(
        default=None,
        alias="welcomeUrl",
        description="Welcome page URL",
    )
    contact_url: str | None = Field(
        default=None,
        alias="contactUrl",
        description="Contact information URL",
    )
    logo_url: str | None = Field(
        default=None,
        alias="logoUrl",
        description="Organization logo URL",
    )
    info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional organization metadata",
    )


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
    info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional beacon metadata",
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

    model_config = {"populate_by_name": True}

    exists: bool = Field(
        ...,
        description="Whether any results were found",
    )
    num_total_results: int | None = Field(
        default=None,
        alias="numTotalResults",
        description="Total number of results",
    )


class ResultsetInstance(BaseModel):
    """Single result instance from a Beacon query."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Result identifier")
    set_type: str = Field(
        ...,
        alias="setType",
        description="Type of the result set",
        examples=["dataset", "individual", "biosample"],
    )
    exists: bool = Field(..., description="Whether results exist in this set")
    result_count: int | None = Field(
        default=None,
        alias="resultsCount",
        description="Number of results in this set",
    )
    results: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Actual result records",
    )
    info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional information about the result set",
    )
    results_handover: list[dict[str, Any]] = Field(
        default_factory=list,
        alias="resultsHandovers",
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
    returned_schemas: list[SchemaReference] = Field(
        default_factory=list,
        alias="returnedSchemas",
        description="Schemas used in the response",
    )
    test_mode: bool = Field(
        default=False,
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
        default_factory=dict,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] | None = Field(
        default_factory=list,
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
    info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] = Field(
        default_factory=list,
        alias="beaconHandovers",
        description="Handovers for accessing data externally",
    )
    beacon_error: BeaconError | None = Field(
        default=None,
        alias="beaconError",
        description="Error information if query failed",
    )


class BeaconResultsetsResponseBody(BaseModel):
    """Resultsets container for record-level responses."""

    model_config = {"populate_by_name": True}

    result_sets: list[ResultsetInstance] = Field(
        default_factory=list,
        alias="resultSets",
        description="Result sets",
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
    response: BeaconResultsetsResponseBody | None = Field(
        default=None,
        description="Result sets",
    )
    info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] = Field(
        default_factory=list,
        alias="beaconHandovers",
        description="Handovers for accessing data externally",
    )
    beacon_error: BeaconError | None = Field(
        default=None,
        alias="beaconError",
        description="Error information if query failed",
    )


class BeaconCollectionsResponseBody(BaseModel):
    """Collections container for collections responses."""

    model_config = {"populate_by_name": True}

    collections: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Collections returned by the beacon",
    )


class BeaconCollectionsResponse(BaseModel):
    """Collections response from Beacon."""

    model_config = {"populate_by_name": True}

    meta: BeaconResponseMeta = Field(..., description="Response metadata")
    response_summary: BeaconSummaryResults = Field(
        ...,
        alias="responseSummary",
        description="Summary of query results",
    )
    response: BeaconCollectionsResponseBody = Field(
        ...,
        description="Collections payload",
    )
    info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional information",
    )
    beacon_handovers: list[BeaconHandover] = Field(
        default_factory=list,
        alias="beaconHandovers",
        description="Handovers for accessing data externally",
    )
