"""Beacon v2 entity models (individuals, biosamples, variations, etc.)."""

from typing import Any

from pydantic import BaseModel, Field


class Individual(BaseModel):
    """Individual/subject entity model."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Individual identifier")
    sex: dict[str, Any] | None = Field(
        default=None,
        description="Sex of the individual (ontology term)",
    )
    karyotypic_sex: str | None = Field(
        default=None,
        alias="karyotypicSex",
        description="Chromosomal sex",
        examples=["XX", "XY", "XO", "XXY", "XXXY"],
    )
    ethnicity: dict[str, Any] | None = Field(
        default=None,
        description="Ethnic background ontology term",
    )
    geographic_origin: dict[str, Any] | None = Field(
        default=None,
        alias="geographicOrigin",
        description="Geographic origin ontology term",
    )
    diseases: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of diseases associated with the individual",
    )
    phenotypic_features: list[dict[str, Any]] | None = Field(
        default=None,
        alias="phenotypicFeatures",
        description="List of phenotypic features",
    )
    interventions_or_procedures: list[dict[str, Any]] | None = Field(
        default=None,
        alias="interventionsOrProcedures",
        description="List of interventions or procedures",
    )
    exposures: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of exposures",
    )
    treatments: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of treatments",
    )
    pedigrees: list[dict[str, Any]] | None = Field(
        default=None,
        description="Pedigree information",
    )
    measurements: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of measurements",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Biosample(BaseModel):
    """Biosample entity model."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Biosample identifier")
    individual_id: str | None = Field(
        default=None,
        alias="individualId",
        description="Reference to the individual this biosample was derived from",
    )
    biosample_status: dict[str, Any] | None = Field(
        default=None,
        alias="biosampleStatus",
        description="Status of the biosample",
    )
    sample_origin_type: dict[str, Any] | None = Field(
        default=None,
        alias="sampleOriginType",
        description="Type of sample origin",
    )
    sample_origin_detail: dict[str, Any] | None = Field(
        default=None,
        alias="sampleOriginDetail",
        description="Detailed information about sample origin",
    )
    collection_date: str | None = Field(
        default=None,
        alias="collectionDate",
        description="Date when the sample was collected",
    )
    collection_moment: str | None = Field(
        default=None,
        alias="collectionMoment",
        description="Moment in time when sample was collected",
    )
    obtention_procedure: dict[str, Any] | None = Field(
        default=None,
        alias="obtentionProcedure",
        description="Procedure used to obtain the sample",
    )
    phenotypic_features: list[dict[str, Any]] | None = Field(
        default=None,
        alias="phenotypicFeatures",
        description="List of phenotypic features",
    )
    measurements: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of measurements",
    )
    histological_diagnosis: dict[str, Any] | None = Field(
        default=None,
        alias="histologicalDiagnosis",
        description="Histological diagnosis (ontology term)",
    )
    pathological_stage: dict[str, Any] | None = Field(
        default=None,
        alias="pathologicalStage",
        description="Pathological stage of the sample",
    )
    pathological_tnm_finding: list[dict[str, Any]] | None = Field(
        default=None,
        alias="pathologicalTnmFinding",
        description="TNM pathological findings",
    )
    tumor_progression: dict[str, Any] | None = Field(
        default=None,
        alias="tumorProgression",
        description="Tumor progression status",
    )
    tumor_grade: dict[str, Any] | None = Field(
        default=None,
        alias="tumorGrade",
        description="Tumor grade",
    )
    diagnostic_markers: list[dict[str, Any]] | None = Field(
        default=None,
        alias="diagnosticMarkers",
        description="List of diagnostic markers",
    )
    sample_processing: dict[str, Any] | None = Field(
        default=None,
        alias="sampleProcessing",
        description="Sample processing information",
    )
    sample_storage: dict[str, Any] | None = Field(
        default=None,
        alias="sampleStorage",
        description="Sample storage conditions",
    )
    notes: str | None = Field(
        default=None,
        description="Additional notes about the biosample",
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

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Analysis identifier")
    analysis_date: str | None = Field(
        default=None,
        alias="analysisDate",
        description="Date when the analysis was performed",
    )
    pipeline_name: str | None = Field(
        default=None,
        alias="pipelineName",
        description="Name of the analysis pipeline",
    )
    pipeline_ref: str | None = Field(
        default=None,
        alias="pipelineRef",
        description="Reference to the pipeline (e.g., URL, DOI)",
    )
    aligner: str | None = Field(
        default=None,
        description="Aligner used in the analysis",
    )
    variant_caller: str | None = Field(
        default=None,
        alias="variantCaller",
        description="Variant caller used in the analysis",
    )
    biosample_id: str | None = Field(
        default=None,
        alias="biosampleId",
        description="Reference to the biosample analyzed",
    )
    individual_id: str | None = Field(
        default=None,
        alias="individualId",
        description="Reference to the individual analyzed",
    )
    run_id: str | None = Field(
        default=None,
        alias="runId",
        description="Reference to the sequencing run",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Cohort(BaseModel):
    """Cohort entity model."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Cohort identifier")
    name: str = Field(..., description="Cohort name")
    cohort_type: str | None = Field(
        default=None,
        alias="cohortType",
        description="Type of cohort",
        examples=["study-defined", "beacon-defined"],
    )
    cohort_design: dict[str, Any] | None = Field(
        default=None,
        alias="cohortDesign",
        description="Cohort design (ontology term)",
    )
    cohort_size: int | None = Field(
        default=None,
        alias="cohortSize",
        description="Number of individuals in the cohort",
        ge=0,
    )
    cohort_data_types: list[dict[str, Any]] | None = Field(
        default=None,
        alias="cohortDataTypes",
        description="Types of data available for this cohort",
    )
    collection_events: list[dict[str, Any]] | None = Field(
        default=None,
        alias="collectionEvents",
        description="Collection events for this cohort",
    )
    inclusion_criteria: dict[str, Any] | None = Field(
        default=None,
        alias="inclusionCriteria",
        description="Inclusion criteria for the cohort",
    )
    exclusion_criteria: dict[str, Any] | None = Field(
        default=None,
        alias="exclusionCriteria",
        description="Exclusion criteria for the cohort",
    )


class Dataset(BaseModel):
    """Dataset entity model."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Dataset identifier")
    name: str = Field(..., description="Dataset name")
    description: str | None = Field(
        default=None,
        description="Dataset description",
    )
    create_date_time: str | None = Field(
        default=None,
        alias="createDateTime",
        description="Dataset creation date and time",
    )
    update_date_time: str | None = Field(
        default=None,
        alias="updateDateTime",
        description="Dataset last update date and time",
    )
    version: str | None = Field(
        default=None,
        description="Dataset version",
    )
    external_url: str | None = Field(
        default=None,
        alias="externalUrl",
        description="External URL for the dataset",
    )
    data_use_conditions: dict[str, Any] | None = Field(
        default=None,
        alias="dataUseConditions",
        description="Data use conditions and restrictions",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )


class Run(BaseModel):
    """Sequencing run entity model."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Run identifier")
    biosample_id: str | None = Field(
        default=None,
        alias="biosampleId",
        description="Reference to the biosample sequenced",
    )
    individual_id: str | None = Field(
        default=None,
        alias="individualId",
        description="Reference to the individual sequenced",
    )
    run_date: str | None = Field(
        default=None,
        alias="runDate",
        description="Date when the run was performed",
    )
    library_source: dict[str, Any] | None = Field(
        default=None,
        alias="librarySource",
        description="Source of the library (ontology term)",
    )
    library_selection: str | None = Field(
        default=None,
        alias="librarySelection",
        description="Library selection method",
    )
    library_strategy: str | None = Field(
        default=None,
        alias="libraryStrategy",
        description="Library strategy",
        examples=["WGS", "WXS", "RNA-Seq", "ChIP-Seq"],
    )
    library_layout: str | None = Field(
        default=None,
        alias="libraryLayout",
        description="Library layout",
        examples=["SINGLE", "PAIRED"],
    )
    platform: str | None = Field(
        default=None,
        description="Sequencing platform",
        examples=["ILLUMINA", "PACBIO", "OXFORD_NANOPORE"],
    )
    platform_model: dict[str, Any] | None = Field(
        default=None,
        alias="platformModel",
        description="Specific platform model (ontology term)",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="Additional information",
    )
