"""Base service interfaces for Beacon v2 entities.

These abstract base classes define the contract for implementing
entity-specific services. Implementers should subclass these and
provide concrete implementations for their database/storage backend.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from beacon_api.models.entities import (
    Analysis,
    Biosample,
    Cohort,
    Dataset,
    GenomicVariation,
    Individual,
    Run,
)
from beacon_api.models.request import BeaconRequestBody


class BaseBeaconService(ABC):
    """Base interface for all Beacon services."""

    @abstractmethod
    async def count(
        self,
        request_body: BeaconRequestBody,
    ) -> int:
        """
        Count results matching the query.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            Number of matching results

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    @abstractmethod
    async def exists(
        self,
        request_body: BeaconRequestBody,
    ) -> bool:
        """
        Check if any results match the query.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            True if any results exist, False otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass


class IndividualService(BaseBeaconService):
    """Service interface for Individual entity operations."""

    @abstractmethod
    async def get_by_id(self, individual_id: str) -> Individual | None:
        """
        Retrieve an individual by ID.

        Args:
            individual_id: Unique identifier for the individual

        Returns:
            Individual object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Individual]:
        """
        Query individuals based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching Individual objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class BiosampleService(BaseBeaconService):
    """Service interface for Biosample entity operations."""

    @abstractmethod
    async def get_by_id(self, biosample_id: str) -> Biosample | None:
        """
        Retrieve a biosample by ID.

        Args:
            biosample_id: Unique identifier for the biosample

        Returns:
            Biosample object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Biosample]:
        """
        Query biosamples based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching Biosample objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class GenomicVariationService(BaseBeaconService):
    """Service interface for GenomicVariation entity operations."""

    @abstractmethod
    async def get_by_id(self, variation_id: str) -> GenomicVariation | None:
        """
        Retrieve a genomic variation by ID.

        Args:
            variation_id: Unique identifier for the variation

        Returns:
            GenomicVariation object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[GenomicVariation]:
        """
        Query genomic variations based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching GenomicVariation objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class AnalysisService(BaseBeaconService):
    """Service interface for Analysis entity operations."""

    @abstractmethod
    async def get_by_id(self, analysis_id: str) -> Analysis | None:
        """
        Retrieve an analysis by ID.

        Args:
            analysis_id: Unique identifier for the analysis

        Returns:
            Analysis object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Analysis]:
        """
        Query analyses based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching Analysis objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class CohortService(BaseBeaconService):
    """Service interface for Cohort entity operations."""

    @abstractmethod
    async def get_by_id(self, cohort_id: str) -> Cohort | None:
        """
        Retrieve a cohort by ID.

        Args:
            cohort_id: Unique identifier for the cohort

        Returns:
            Cohort object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Cohort]:
        """
        Query cohorts based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching Cohort objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class DatasetService(BaseBeaconService):
    """Service interface for Dataset entity operations."""

    @abstractmethod
    async def get_by_id(self, dataset_id: str) -> Dataset | None:
        """
        Retrieve a dataset by ID.

        Args:
            dataset_id: Unique identifier for the dataset

        Returns:
            Dataset object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Dataset]:
        """
        Query datasets based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching Dataset objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class RunService(BaseBeaconService):
    """Service interface for Run entity operations."""

    @abstractmethod
    async def get_by_id(self, run_id: str) -> Run | None:
        """
        Retrieve a run by ID.

        Args:
            run_id: Unique identifier for the run

        Returns:
            Run object if found, None otherwise

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Run]:
        """
        Query runs based on Beacon request.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            List of matching Run objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError
