"""Beacon v2 request models."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class RequestedGranularity(str, Enum):
    """Requested granularity of the response."""

    BOOLEAN = "boolean"
    COUNT = "count"
    RECORD = "record"


class OntologyFilter(BaseModel):
    """Ontology-based filter."""

    id: str = Field(
        ...,
        description="Ontology term ID",
        examples=["HP:0001250", "NCIT:C3058"],
    )
    scope: Optional[str] = Field(
        default=None,
        description="Scope of the ontology filter",
        examples=["individuals", "biosamples"],
    )
    include_descendant_terms: bool = Field(
        default=False,
        description="Include descendant terms in the query",
    )
    similarity: Optional[str] = Field(
        default=None,
        description="Similarity matching method",
        examples=["exact", "high", "medium", "low"],
    )


class FilteringTerm(BaseModel):
    """Generic filtering term for Beacon queries."""

    type: str = Field(
        ...,
        description="Type of the filter",
        examples=["ontology", "alphanumeric", "numeric"],
    )
    id: Optional[str] = Field(
        default=None,
        description="Filter ID (for ontology filters)",
        examples=["HP:0001250"],
    )
    operator: Optional[str] = Field(
        default=None,
        description="Comparison operator",
        examples=["=", ">", "<", ">=", "<="],
    )
    value: Optional[Any] = Field(
        default=None,
        description="Filter value",
    )
    scope: Optional[str] = Field(
        default=None,
        description="Scope of the filter",
        examples=["individuals", "biosamples"],
    )


class BeaconRequestParameters(BaseModel):
    """Common request parameters for Beacon queries."""

    requested_granularity: RequestedGranularity = Field(
        default=RequestedGranularity.BOOLEAN,
        description="Requested granularity of the response",
    )
    include_resultset_responses: Optional[str] = Field(
        default="HIT",
        description="Defines the level of detail in the response",
        examples=["HIT", "ALL", "MISS", "NONE"],
    )
    pagination: Optional[dict[str, int]] = Field(
        default=None,
        description="Pagination parameters",
        examples=[{"skip": 0, "limit": 10}],
    )


class BeaconQuery(BaseModel):
    """Beacon query parameters for genomic variations."""

    assembly_id: Optional[str] = Field(
        default=None,
        description="Assembly identifier (GRC notation)",
        examples=["GRCh38", "GRCh37"],
    )
    reference_name: Optional[str] = Field(
        default=None,
        description="Reference sequence name",
        examples=["1", "22", "X", "Y", "MT", "chr1"],
    )
    reference_bases: Optional[str] = Field(
        default=None,
        description="Reference bases",
        examples=["A", "T", "C", "G"],
    )
    alternate_bases: Optional[str] = Field(
        default=None,
        description="Alternate bases",
        examples=["A", "T", "C", "G"],
    )
    start: Optional[list[int]] = Field(
        default=None,
        description="Start position(s) in 0-based coordinates",
        examples=[[100000, 200000]],
    )
    end: Optional[list[int]] = Field(
        default=None,
        description="End position(s) in 0-based coordinates",
        examples=[[100100, 200100]],
    )
    variant_type: Optional[str] = Field(
        default=None,
        description="Type of variant",
        examples=["SNP", "DEL", "INS", "DUP", "INV", "CNV"],
    )
    variant_min_length: Optional[int] = Field(
        default=None,
        description="Minimum length of the variant",
        ge=0,
    )
    variant_max_length: Optional[int] = Field(
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
    query: Optional[BeaconQuery] = Field(
        default=None,
        description="Query parameters",
    )
    filters: Optional[list[FilteringTerm]] = Field(
        default=None,
        description="Filtering terms to apply",
    )
