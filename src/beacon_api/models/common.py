"""Common Beacon v2 models and shared schemas."""

from typing import Any

from pydantic import BaseModel, Field


class BeaconError(BaseModel):
    """Beacon error response model."""

    error_code: int = Field(
        ...,
        description="HTTP error code",
        examples=[400, 401, 403, 404, 500],
    )
    error_message: str = Field(
        ...,
        description="Error message",
        examples=["Bad request", "Unauthorized"],
    )


class Pagination(BaseModel):
    """Pagination parameters for list responses."""

    skip: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip",
        examples=[0, 10, 20],
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return",
        examples=[10, 25, 50],
    )


class ListingQuery(BaseModel):
    """Query parameters for listing endpoints."""

    pagination: Pagination | None = Field(
        default=None,
        description="Pagination parameters",
    )
    filters: list[dict[str, Any]] | None = Field(
        default=None,
        description="Filtering terms to apply",
    )


class SchemaReference(BaseModel):
    """Reference to a schema definition."""

    schema_name: str = Field(
        ...,
        description="Name of the schema",
        examples=["beacon-individual-v2.0.0"],
    )
    schema_version: str = Field(
        ...,
        description="Version of the schema",
        examples=["2.0.0"],
    )
    schema_url: str | None = Field(
        default=None,
        description="URL to the schema definition",
        examples=[
            "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2/main/models/json/beacon-v2-default-model/individuals/defaultSchema.json"
        ],
    )
