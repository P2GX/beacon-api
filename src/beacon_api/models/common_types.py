"""Common types for Beacon v2 models.

These types are extracted from the Beacon v2 JSON schemas and provide
proper validation for nested structures used across entity models.

Generated from beacon-v2 schemas with manual deduplication and cleanup.
"""

from __future__ import annotations

from datetime import date as date_type
from enum import StrEnum

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class OntologyTerm(BaseModel):
    """Ontology term with CURIE identifier.

    Used throughout Beacon for controlled vocabulary terms (sex, ethnicity,
    disease codes, phenotype features, etc.).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        ...,
        pattern=r"^\w[^:]+:.+$",
        description="CURIE identifier (e.g., 'HP:0001250', 'NCIT:C20197')",
        examples=[
            "ga4gh:GA.01234abcde",
            "DUO:0000004",
            "orcid:0000-0003-3463-0775",
            "PMID:15254584",
        ],
    )
    label: str | None = Field(
        default=None,
        description="Human-readable label for the term",
    )


class Age(BaseModel):
    """Age as ISO8601 duration.

    Provenance: GA4GH Phenopackets v2 `Age`
    """

    model_config = ConfigDict(populate_by_name=True)

    iso8601duration: str | None = Field(
        default=None,
        description="Age as ISO8601 duration (e.g., P40Y10M05D)",
        examples=["P32Y6M1D", "P25Y", "P3M"],
    )


class AgeRange(BaseModel):
    """Age range with start and end.

    Provenance: GA4GH Phenopackets v2 `AgeRange`
    """

    model_config = ConfigDict(populate_by_name=True)

    start: Age | None = Field(default=None, description="Start of age range")
    end: Age | None = Field(default=None, description="End of age range")


class GestationalAge(BaseModel):
    """Gestational age in weeks and days.

    Provenance: GA4GH Phenopackets v2
    """

    model_config = ConfigDict(populate_by_name=True)

    weeks: int = Field(
        ..., description="Completed weeks of gestation", examples=[4, 33]
    )
    days: int | None = Field(
        default=None,
        description="Days beyond completed weeks",
        examples=[2, 4],
    )


class TimeInterval(BaseModel):
    """Time interval with ISO8601 timestamps."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    start: AwareDatetime = Field(
        ...,
        description="Start time in ISO8601 format",
        examples=["1999-08-05T17:21:00+01:00"],
    )
    end: AwareDatetime = Field(
        ...,
        description="End time in ISO8601 format",
        examples=["2002-09-21T02:37:00-08:00"],
    )


# Union type for time-related fields (ageOfOnset, onset, resolution, etc.)
TimeElement = (
    Age | AgeRange | GestationalAge | AwareDatetime | TimeInterval | OntologyTerm
)


class KaryotypicSex(StrEnum):
    """Chromosomal sex of an individual."""

    UNKNOWN_KARYOTYPE = "UNKNOWN_KARYOTYPE"
    XX = "XX"
    XY = "XY"
    XO = "XO"
    XXY = "XXY"
    XXX = "XXX"
    XXYY = "XXYY"
    XXXY = "XXXY"
    XXXX = "XXXX"
    XYY = "XYY"
    OTHER_KARYOTYPE = "OTHER_KARYOTYPE"


class ReferenceRange(BaseModel):
    """Reference range for measurements."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    low: float = Field(..., description="Lower range end of normal", examples=[85])
    high: float = Field(..., description="Upper range end of normal", examples=[135])
    unit: OntologyTerm = Field(..., description="Unit of measurement")


class Quantity(BaseModel):
    """Quantity with value, unit, and optional reference range.

    Provenance: GA4GH Phenopackets v2 `Quantity`
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    value: float = Field(..., description="The value of the quantity")
    unit: OntologyTerm = Field(..., description="Unit of measurement")
    reference_range: ReferenceRange | None = Field(
        default=None,
        alias="referenceRange",
        description="Normal range for this measurement",
    )


class TypedQuantity(BaseModel):
    """Quantity with an associated type."""

    model_config = ConfigDict(populate_by_name=True)

    quantity: Quantity = Field(..., description="The quantity value")
    quantity_type: OntologyTerm = Field(
        ...,
        alias="quantityType",
        description="Type of quantity being measured",
        examples=[{"id": "NCIT:C25298", "label": "Systolic Blood Pressure"}],
    )


class ComplexValue(BaseModel):
    """Complex measurement value with multiple typed quantities."""

    model_config = ConfigDict(populate_by_name=True)

    typed_quantities: list[TypedQuantity] | None = Field(
        default=None,
        alias="typedQuantities",
        description="List of quantities for complex measurements",
    )


class ExternalReference(BaseModel):
    """Reference to external resource."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None,
        description="External identifier",
        examples=["PMID:34054918"],
    )
    reference: str | None = Field(
        default=None,
        description="URL to the resource",
        examples=["https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8155688/"],
    )
    notes: str | None = Field(
        default=None,
        description="Additional notes about the reference",
    )


class Evidence(BaseModel):
    """Evidence for an assertion."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    evidence_code: OntologyTerm = Field(
        ...,
        alias="evidenceCode",
        description="Evidence type ontology term",
        examples=[
            {
                "id": "ECO:0006017",
                "label": "author statement from published clinical study",
            }
        ],
    )
    reference: ExternalReference | None = Field(
        default=None,
        description="Source of the evidence",
    )


class Procedure(BaseModel):
    """Clinical procedure or intervention.

    Provenance: GA4GH Phenopackets v2 `Procedure`
    """

    model_config = ConfigDict(populate_by_name=True)

    procedure_code: OntologyTerm = Field(
        ...,
        alias="procedureCode",
        description="Procedure ontology term",
        examples=[
            {"id": "MAXO:0001175", "label": "liver transplantation"},
            {"id": "OBI:0002654", "label": "needle biopsy"},
        ],
    )
    body_site: OntologyTerm | None = Field(
        default=None,
        alias="bodySite",
        description="Body site where procedure was performed",
        examples=[{"id": "UBERON:0003403", "label": "Skin of forearm"}],
    )
    date_of_procedure: date_type | None = Field(
        default=None,
        alias="dateOfProcedure",
        description="Date of procedure in ISO8601 format",
        examples=["2010-07-10"],
    )
    age_at_procedure: TimeElement | None = Field(
        default=None,
        alias="ageAtProcedure",
        description="Age when procedure was performed",
    )


class Disease(BaseModel):
    """Disease diagnosed to an individual.

    Similarities to GA4GH Phenopackets v2 `Disease`
    """

    model_config = ConfigDict(populate_by_name=True)

    disease_code: OntologyTerm = Field(
        ...,
        alias="diseaseCode",
        description="Disease ontology term",
        examples=[
            {"id": "HP:0004789", "label": "lactose intolerance"},
            {"id": "OMIM:164400", "label": "Spinocerebellar ataxia 1"},
        ],
    )
    age_of_onset: TimeElement | None = Field(
        default=None,
        alias="ageOfOnset",
        description="Age or time when disease was first observed",
    )
    stage: OntologyTerm | None = Field(
        default=None,
        description="Disease stage",
        examples=[
            {"id": "OGMS:0000119", "label": "acute onset"},
            {"id": "OGMS:0000117", "label": "asymptomatic"},
        ],
    )
    severity: OntologyTerm | None = Field(
        default=None,
        description="Disease severity",
        examples=[
            {"id": "HP:0012828", "label": "Severe"},
            {"id": "HP:0012826", "label": "Moderate"},
        ],
    )
    family_history: bool | None = Field(
        default=None,
        alias="familyHistory",
        description="Presence of family history of this disease",
    )
    notes: str | None = Field(
        default=None,
        description="Additional notes about the disease",
    )


class PhenotypicFeature(BaseModel):
    """Phenotypic feature observed in an individual or biosample.

    Provenance: GA4GH Phenopackets v2 `PhenotypicFeature`
    """

    model_config = ConfigDict(populate_by_name=True)

    feature_type: OntologyTerm = Field(
        ...,
        alias="featureType",
        description="Phenotype ontology term",
        examples=[
            {"id": "HP:0000002", "label": "Abnormality of body height"},
            {"id": "HP:0012469", "label": "Infantile spasms"},
        ],
    )
    excluded: bool | None = Field(
        default=False,
        description="True if the feature was looked for but not found",
    )
    onset: TimeElement | None = Field(
        default=None,
        description="Age or time when feature was first observed",
    )
    resolution: TimeElement | None = Field(
        default=None,
        description="Age or time when feature resolved",
    )
    severity: OntologyTerm | None = Field(
        default=None,
        description="Severity of the phenotypic feature",
    )
    modifiers: list[OntologyTerm] | None = Field(
        default=None,
        description="Modifier terms (e.g., laterality, severity qualifiers)",
    )
    evidence: Evidence | None = Field(
        default=None,
        description="Evidence for this phenotypic feature",
    )
    notes: str | None = Field(
        default=None,
        description="Additional notes",
    )


class Exposure(BaseModel):
    """Environmental or other exposure."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    exposure_code: OntologyTerm = Field(
        ...,
        alias="exposureCode",
        description="Exposure type ontology term",
        examples=[
            {"id": "CHEBI:46661", "label": "asbestos"},
            {"id": "ENVO:21001217", "label": "X-ray radiation"},
        ],
    )
    age_at_exposure: Age = Field(
        ...,
        alias="ageAtExposure",
        description="Age at time of exposure",
    )
    duration: str = Field(
        ...,
        description="Exposure duration in ISO8601 format",
        examples=["P32Y6M1D"],
    )
    unit: OntologyTerm = Field(..., description="Unit of exposure measurement")
    value: float | None = Field(
        default=None,
        description="Quantification of the exposure",
    )
    date: date_type | None = Field(
        default=None,
        description="Date of exposure in ISO8601 format",
    )


class DoseInterval(BaseModel):
    """Dose interval for treatments."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    interval: TimeInterval = Field(..., description="Time interval for dosing")
    quantity: Quantity = Field(..., description="Dose quantity")
    schedule_frequency: OntologyTerm = Field(
        ...,
        alias="scheduleFrequency",
        description="Dosing frequency",
        examples=[{"id": "NCIT:C64496", "label": "Twice Daily"}],
    )


class Treatment(BaseModel):
    """Treatment administered to an individual."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    treatment_code: OntologyTerm = Field(
        ...,
        alias="treatmentCode",
        description="Treatment ontology term",
        examples=[
            {"id": "NCIT:C287", "label": "Aspirin"},
            {"id": "NCIT:C62078", "label": "Tamoxifen"},
        ],
    )
    age_at_onset: Age | None = Field(
        default=None,
        alias="ageAtOnset",
        description="Age when treatment started",
    )
    route_of_administration: OntologyTerm | None = Field(
        default=None,
        alias="routeOfAdministration",
        description="Route of administration",
        examples=[{"id": "NCIT:C38304", "label": "Topical"}],
    )
    cumulative_dose: Quantity | None = Field(
        default=None,
        alias="cumulativeDose",
        description="Total cumulative dose",
    )
    dose_intervals: list[DoseInterval] | None = Field(
        default=None,
        alias="doseIntervals",
        description="Dose intervals",
    )


class Measurement(BaseModel):
    """Measurement performed on an individual or biosample.

    Provenance: GA4GH Phenopackets v2 `Measurement`
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    assay_code: OntologyTerm = Field(
        ...,
        alias="assayCode",
        description="Assay ontology term",
        examples=[{"id": "LOINC:26515-7", "label": "Platelets [#/volume] in Blood"}],
    )
    measurement_value: ComplexValue | Quantity | OntologyTerm = Field(
        ...,
        alias="measurementValue",
        description="Result of the measurement",
    )
    observation_moment: TimeElement | None = Field(
        default=None,
        alias="observationMoment",
        description="Time when measurement was performed",
    )
    procedure: Procedure | None = Field(
        default=None,
        description="Procedure used for measurement",
    )
    date: date_type | None = Field(
        default=None,
        description="Date of measurement",
    )
    notes: str | None = Field(
        default=None,
        description="Additional notes",
    )


class Member(BaseModel):
    """Member of a pedigree."""

    model_config = ConfigDict(populate_by_name=True)

    member_id: str = Field(
        ...,
        alias="memberId",
        description="Identifier of the pedigree member",
        examples=["Pedigree1001-m1", "Ind0012122"],
    )
    role: OntologyTerm = Field(
        ...,
        description="Role in the pedigree",
        examples=[
            {"id": "NCIT:C64435", "label": "Proband"},
            {"id": "NCIT:C96580", "label": "Biological Mother"},
        ],
    )
    affected: bool = Field(
        ...,
        description="Whether member is affected by the disease",
    )


class Pedigree(BaseModel):
    """Pedigree information for an individual."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(..., description="Pedigree identifier", examples=["Pedigree1001"])
    disease: Disease = Field(..., description="Disease tracked in this pedigree")
    members: list[Member] = Field(
        ...,
        min_length=1,
        description="Members of the pedigree",
    )
    num_subjects: int | None = Field(
        default=None,
        alias="numSubjects",
        description="Total number of subjects in pedigree",
    )
