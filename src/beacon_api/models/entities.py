"""Beacon v2 entity models (individuals, biosamples, variations, etc.)."""

from typing import Any

from pydantic import BaseModel, Field


class Individual(BaseModel):
    """Individual/subject entity model."""

    id: str = Field(..., description="Individual identifier")
    sex: str | None = Field(
        default=None,
        description="Sex of the individual",
        examples=["MALE", "FEMALE", "OTHER_SEX", "UNKNOWN_SEX"],
    )
    ethnicity: dict[str, Any] | None = Field(
        default=None,
        description="Ethnic background ontology term",
    )
    geographic_origin: dict[str, Any] | None = Field(
        default=None,
        description="Geographic origin ontology term",
    )
    diseases: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of diseases associated with the individual",
    )
    phenotypic_features: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of phenotypic features",
    )
    interventions_or_procedures: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of interventions or procedures",
    )
    measures: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of measurements",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Biosample(BaseModel):
    """Biosample entity model."""

    id: str = Field(..., description="Biosample identifier")
    individual_id: str | None = Field(
        default=None,
        description="Reference to the individual this biosample was derived from",
    )
    biosample_status: dict[str, Any] | None = Field(
        default=None,
        description="Status of the biosample",
    )
    sample_origin_type: dict[str, Any] | None = Field(
        default=None,
        description="Type of sample origin",
    )
    sample_origin_detail: dict[str, Any] | None = Field(
        default=None,
        description="Detailed information about sample origin",
    )
    collection_date: str | None = Field(
        default=None,
        description="Date when the sample was collected",
    )
    collection_moment: str | None = Field(
        default=None,
        description="Moment in time when sample was collected",
    )
    obtained_from_id: str | None = Field(
        default=None,
        description="ID of the biosample this sample was obtained from",
    )
    phenotypic_features: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of phenotypic features",
    )
    measurements: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of measurements",
    )
    pathological_stage: dict[str, Any] | None = Field(
        default=None,
        description="Pathological stage of the sample",
    )
    tumor_progression: dict[str, Any] | None = Field(
        default=None,
        description="Tumor progression status",
    )
    tumor_grade: dict[str, Any] | None = Field(
        default=None,
        description="Tumor grade",
    )
    diagnostic_markers: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of diagnostic markers",
    )
    procedure: dict[str, Any] | None = Field(
        default=None,
        description="Procedure used to collect the sample",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class GenomicVariation(BaseModel):
    """Genomic variation entity model."""

    id: str = Field(..., description="Variation identifier")
    variation_type: str | None = Field(
        default=None,
        description="Type of variation",
        examples=["SNP", "DEL", "INS", "DUP", "INV", "CNV"],
    )
    reference_genome: str | None = Field(
        default=None,
        description="Reference genome assembly",
        examples=["GRCh38", "GRCh37"],
    )
    chromosome: str | None = Field(
        default=None,
        description="Chromosome name",
        examples=["1", "22", "X", "Y", "MT"],
    )
    start: int | None = Field(
        default=None,
        description="Start position (0-based)",
        ge=0,
    )
    end: int | None = Field(
        default=None,
        description="End position (0-based)",
        ge=0,
    )
    reference_bases: str | None = Field(
        default=None,
        description="Reference bases",
    )
    alternate_bases: str | None = Field(
        default=None,
        description="Alternate bases",
    )
    variant_internal_id: str | None = Field(
        default=None,
        description="Internal variant identifier",
    )
    identifiers: dict[str, Any] | None = Field(
        default=None,
        description="External identifiers for this variation",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Analysis(BaseModel):
    """Analysis entity model."""

    id: str = Field(..., description="Analysis identifier")
    analysis_type: dict[str, Any] | None = Field(
        default=None,
        description="Type of analysis performed",
    )
    pipeline_name: str | None = Field(
        default=None,
        description="Name of the analysis pipeline",
    )
    pipeline_ref: str | None = Field(
        default=None,
        description="Reference to the pipeline (e.g., URL, DOI)",
    )
    analysis_date: str | None = Field(
        default=None,
        description="Date when the analysis was performed",
    )
    biosample_id: str | None = Field(
        default=None,
        description="Reference to the biosample analyzed",
    )
    individual_id: str | None = Field(
        default=None,
        description="Reference to the individual analyzed",
    )
    run_id: str | None = Field(
        default=None,
        description="Reference to the sequencing run",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Cohort(BaseModel):
    """Cohort entity model."""

    id: str = Field(..., description="Cohort identifier")
    name: str = Field(..., description="Cohort name")
    cohort_type: str | None = Field(
        default=None,
        description="Type of cohort",
        examples=["study-defined", "beacon-defined"],
    )
    cohort_size: int | None = Field(
        default=None,
        description="Number of individuals in the cohort",
        ge=0,
    )
    cohort_data_types: list[dict[str, Any]] | None = Field(
        default=None,
        description="Types of data available for this cohort",
    )
    collection_events: list[dict[str, Any]] | None = Field(
        default=None,
        description="Collection events for this cohort",
    )
    inclusion_criteria: dict[str, Any] | None = Field(
        default=None,
        description="Inclusion criteria for the cohort",
    )
    exclusion_criteria: dict[str, Any] | None = Field(
        default=None,
        description="Exclusion criteria for the cohort",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Dataset(BaseModel):
    """Dataset entity model."""

    id: str = Field(..., description="Dataset identifier")
    name: str = Field(..., description="Dataset name")
    description: str | None = Field(
        default=None,
        description="Dataset description",
    )
    assembly_id: str | None = Field(
        default=None,
        description="Reference genome assembly",
        examples=["GRCh38", "GRCh37"],
    )
    create_date_time: str | None = Field(
        default=None,
        description="Dataset creation date and time",
    )
    update_date_time: str | None = Field(
        default=None,
        description="Dataset last update date and time",
    )
    version: str | None = Field(
        default=None,
        description="Dataset version",
    )
    external_url: str | None = Field(
        default=None,
        description="External URL for the dataset",
    )
    data_use_conditions: dict[str, Any] | None = Field(
        default=None,
        description="Data use conditions and restrictions",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Run(BaseModel):
    """Sequencing run entity model."""

    id: str = Field(..., description="Run identifier")
    biosample_id: str | None = Field(
        default=None,
        description="Reference to the biosample sequenced",
    )
    individual_id: str | None = Field(
        default=None,
        description="Reference to the individual sequenced",
    )
    run_date: str | None = Field(
        default=None,
        description="Date when the run was performed",
    )
    library_source: str | None = Field(
        default=None,
        description="Source of the library",
        examples=["GENOMIC", "TRANSCRIPTOMIC", "METAGENOMIC"],
    )
    library_selection: str | None = Field(
        default=None,
        description="Library selection method",
    )
    library_strategy: str | None = Field(
        default=None,
        description="Library strategy",
        examples=["WGS", "WXS", "RNA-Seq", "ChIP-Seq"],
    )
    library_layout: str | None = Field(
        default=None,
        description="Library layout",
        examples=["SINGLE", "PAIRED"],
    )
    platform: str | None = Field(
        default=None,
        description="Sequencing platform",
        examples=["ILLUMINA", "PACBIO", "OXFORD_NANOPORE"],
    )
    platform_model: str | None = Field(
        default=None,
        description="Specific platform model",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )
