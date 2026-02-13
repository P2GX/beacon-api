"""Beacon v2 request models."""

from enum import StrEnum

from pydantic import BaseModel, Field


class RequestedGranularity(StrEnum):
    """Requested granularity of the response."""

    BOOLEAN = "boolean"
    COUNT = "count"
    RECORD = "record"


class OntologyFilter(BaseModel):
    """Ontology-based filter for Beacon v2.

    Used for bio-ontology term queries identified by CURIE format.
    """

    id: str = Field(
        ...,
        description="Ontology term ID in CURIE format",
        examples=["HP:0001250", "NCIT:C3058", "HP:0100526"],
    )
    includeDescendantTerms: bool = Field(
        default=True,
        description="Include descendant terms in the query (default: true)",
    )
    similarity: str | None = Field(
        default=None,
        description="Similarity matching method",
        examples=["high", "medium", "low"],
    )


class FilteringTerm(BaseModel):
    """Filtering term for Beacon v2 queries.

    Supports three filter types:
    1. Ontology filters: Only 'id' required, optionally with includeDescendantTerms/similarity
    2. Alphanumeric/Numeric filters: Requires 'id', 'operator', and 'value'
    3. Custom filters: Locally-defined with unique identifiers
    """

    id: str = Field(
        ...,
        description="Filter identifier (CURIE for ontology, field ID for alphanumeric)",
        examples=["HP:0001250", "PATO:0000011", "NCIT:C6975"],
    )
    operator: str | None = Field(
        default=None,
        description="Comparison operator for alphanumeric/numeric filters",
        examples=["=", ">", "<", "!", ">=", "<="],
    )
    value: str | int | float | None = Field(
        default=None,
        description="Filter value (ISO8601 for dates, wildcards % supported)",
        examples=["P70Y", "cancer", 100, "%breast%"],
    )
    includeDescendantTerms: bool | None = Field(
        default=None,
        description="For ontology filters: include descendant terms (default: true)",
    )
    similarity: str | None = Field(
        default=None,
        description="For ontology filters: similarity level",
        examples=["high", "medium", "low"],
    )


class BeaconRequestParameters(BaseModel):
    """Common request parameters for Beacon queries."""

    requested_granularity: RequestedGranularity = Field(
        default=RequestedGranularity.BOOLEAN,
        description="Requested granularity of the response",
    )
    include_resultset_responses: str | None = Field(
        default="HIT",
        description="Defines the level of detail in the response",
        examples=["HIT", "ALL", "MISS", "NONE"],
    )
    pagination: dict[str, int] | None = Field(
        default=None,
        description="Pagination parameters",
        examples=[{"skip": 0, "limit": 10}],
    )


class BeaconQuery(BaseModel):
    """Beacon query parameters for genomic variations."""

    assembly_id: str | None = Field(
        default=None,
        description="Assembly identifier (GRC notation)",
        examples=["GRCh38", "GRCh37"],
    )
    reference_name: str | None = Field(
        default=None,
        description="Reference sequence name",
        examples=["1", "22", "X", "Y", "MT", "chr1"],
    )
    reference_bases: str | None = Field(
        default=None,
        description="Reference bases",
        examples=["A", "T", "C", "G"],
    )
    alternate_bases: str | None = Field(
        default=None,
        description="Alternate bases",
        examples=["A", "T", "C", "G"],
    )
    start: list[int] | None = Field(
        default=None,
        description="Start position(s) in 0-based coordinates",
        examples=[[100000, 200000]],
    )
    end: list[int] | None = Field(
        default=None,
        description="End position(s) in 0-based coordinates",
        examples=[[100100, 200100]],
    )
    variant_type: str | None = Field(
        default=None,
        description="Type of variant",
        examples=["SNP", "DEL", "INS", "DUP", "INV", "CNV"],
    )
    variant_min_length: int | None = Field(
        default=None,
        description="Minimum length of the variant",
        ge=0,
    )
    variant_max_length: int | None = Field(
        default=None,
        description="Maximum length of the variant",
        ge=0,
    )


class BeaconRequestBody(BaseModel):
    """Complete Beacon request body."""

    meta: BeaconRequestParameters = Field(
        default_factory=BeaconRequestParameters,
        description="Request metadata and parameters",
    )
    query: BeaconQuery | None = Field(
        default=None,
        description="Query parameters",
    )
    filters: list[FilteringTerm] | None = Field(
        default=None,
        description="Filtering terms to apply",
    )
