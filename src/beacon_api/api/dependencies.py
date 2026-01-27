"""FastAPI dependencies for Beacon API.

This module contains dependency injection functions for services.
Implementers should modify these to return their concrete service implementations.

By default, stub implementations are returned that raise NotImplementedError
when methods are called. This allows the API to start and respond with empty
results for beacon-verifier compliance.
"""

from typing import Annotated

from fastapi import Depends

from beacon_api.services.base import (
    AnalysisService,
    BiosampleService,
    CohortService,
    DatasetService,
    GenomicVariationService,
    IndividualService,
    RunService,
)
from beacon_api.services.stubs import (
    StubAnalysisService,
    StubBiosampleService,
    StubCohortService,
    StubDatasetService,
    StubGenomicVariationService,
    StubIndividualService,
    StubRunService,
)


def get_individual_service() -> IndividualService:
    """
    Dependency for IndividualService.

    Override this function to return your concrete implementation.

    Returns:
        IndividualService instance (stub by default)
    """
    return StubIndividualService()


def get_biosample_service() -> BiosampleService:
    """
    Dependency for BiosampleService.

    Override this function to return your concrete implementation.

    Returns:
        BiosampleService instance (stub by default)
    """
    return StubBiosampleService()


def get_genomic_variation_service() -> GenomicVariationService:
    """
    Dependency for GenomicVariationService.

    Override this function to return your concrete implementation.

    Returns:
        GenomicVariationService instance (stub by default)
    """
    return StubGenomicVariationService()


def get_analysis_service() -> AnalysisService:
    """
    Dependency for AnalysisService.

    Override this function to return your concrete implementation.

    Returns:
        AnalysisService instance (stub by default)
    """
    return StubAnalysisService()


def get_cohort_service() -> CohortService:
    """
    Dependency for CohortService.

    Override this function to return your concrete implementation.

    Returns:
        CohortService instance (stub by default)
    """
    return StubCohortService()


def get_dataset_service() -> DatasetService:
    """
    Dependency for DatasetService.

    Override this function to return your concrete implementation.

    Returns:
        DatasetService instance (stub by default)
    """
    return StubDatasetService()


def get_run_service() -> RunService:
    """
    Dependency for RunService.

    Override this function to return your concrete implementation.

    Returns:
        RunService instance (stub by default)
    """
    return StubRunService()


# Type aliases for cleaner endpoint signatures
IndividualServiceDep = Annotated[IndividualService, Depends(get_individual_service)]
BiosampleServiceDep = Annotated[BiosampleService, Depends(get_biosample_service)]
GenomicVariationServiceDep = Annotated[
    GenomicVariationService, Depends(get_genomic_variation_service)
]
AnalysisServiceDep = Annotated[AnalysisService, Depends(get_analysis_service)]
CohortServiceDep = Annotated[CohortService, Depends(get_cohort_service)]
DatasetServiceDep = Annotated[DatasetService, Depends(get_dataset_service)]
RunServiceDep = Annotated[RunService, Depends(get_run_service)]
