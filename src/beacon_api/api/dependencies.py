"""FastAPI dependencies for Beacon API.

This module contains dependency injection functions for services.
Implementers should modify these to return their concrete service implementations.
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


def get_individual_service() -> IndividualService:
    """
    Dependency for IndividualService.

    Override this function to return your concrete implementation.

    Returns:
        IndividualService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "IndividualService not implemented. "
        "Please provide a concrete implementation in your application."
    )


def get_biosample_service() -> BiosampleService:
    """
    Dependency for BiosampleService.

    Override this function to return your concrete implementation.

    Returns:
        BiosampleService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "BiosampleService not implemented. "
        "Please provide a concrete implementation in your application."
    )


def get_genomic_variation_service() -> GenomicVariationService:
    """
    Dependency for GenomicVariationService.

    Override this function to return your concrete implementation.

    Returns:
        GenomicVariationService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "GenomicVariationService not implemented. "
        "Please provide a concrete implementation in your application."
    )


def get_analysis_service() -> AnalysisService:
    """
    Dependency for AnalysisService.

    Override this function to return your concrete implementation.

    Returns:
        AnalysisService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "AnalysisService not implemented. "
        "Please provide a concrete implementation in your application."
    )


def get_cohort_service() -> CohortService:
    """
    Dependency for CohortService.

    Override this function to return your concrete implementation.

    Returns:
        CohortService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "CohortService not implemented. "
        "Please provide a concrete implementation in your application."
    )


def get_dataset_service() -> DatasetService:
    """
    Dependency for DatasetService.

    Override this function to return your concrete implementation.

    Returns:
        DatasetService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "DatasetService not implemented. "
        "Please provide a concrete implementation in your application."
    )


def get_run_service() -> RunService:
    """
    Dependency for RunService.

    Override this function to return your concrete implementation.

    Returns:
        RunService instance

    Raises:
        NotImplementedError: Default implementation not provided
    """
    raise NotImplementedError(
        "RunService not implemented. "
        "Please provide a concrete implementation in your application."
    )


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
