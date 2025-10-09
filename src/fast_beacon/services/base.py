"""Base service interfaces for Beacon v2 entities.

These abstract base classes define the contract for implementing
entity-specific services. Implementers should subclass these and
provide concrete implementations for their database/storage backend.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from fast_beacon.models.entities import (
    Analysis,
    Biosample,
    Cohort,
    Dataset,
    GenomicVariation,
    Individual,
    Run,
)
from fast_beacon.models.request import BeaconRequestBody, FilteringTerm


class BaseBeaconService(ABC):
    """Base interface for all Beacon services."""

    @abstractmethod
    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> dict[str, Any]:
        """
        Execute a Beacon query.

        Args:
            request_body: Complete Beacon request including query and filters

        Returns:
            Dictionary containing query results

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError


class IndividualService(ABC):
    """Service interface for Individual entity operations."""

    @abstractmethod
    async def get_by_id(self, individual_id: str) -> Optional[Individual]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Individual]:
        """
        List individuals with optional filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filtering terms

        Returns:
            List of Individual objects

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


class BiosampleService(ABC):
    """Service interface for Biosample entity operations."""

    @abstractmethod
    async def get_by_id(self, biosample_id: str) -> Optional[Biosample]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Biosample]:
        """
        List biosamples with optional filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filtering terms

        Returns:
            List of Biosample objects

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


class GenomicVariationService(ABC):
    """Service interface for GenomicVariation entity operations."""

    @abstractmethod
    async def get_by_id(self, variation_id: str) -> Optional[GenomicVariation]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[GenomicVariation]:
        """
        List genomic variations with optional filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filtering terms

        Returns:
            List of GenomicVariation objects

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


class AnalysisService(ABC):
    """Service interface for Analysis entity operations."""

    @abstractmethod
    async def get_by_id(self, analysis_id: str) -> Optional[Analysis]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Analysis]:
        """
        List analyses with optional filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filtering terms

        Returns:
            List of Analysis objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class CohortService(ABC):
    """Service interface for Cohort entity operations."""

    @abstractmethod
    async def get_by_id(self, cohort_id: str) -> Optional[Cohort]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Cohort]:
        """
        List cohorts with optional filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filtering terms

        Returns:
            List of Cohort objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class DatasetService(ABC):
    """Service interface for Dataset entity operations."""

    @abstractmethod
    async def get_by_id(self, dataset_id: str) -> Optional[Dataset]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Dataset]:
        """
        List datasets with optional pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Dataset objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError


class RunService(ABC):
    """Service interface for Run entity operations."""

    @abstractmethod
    async def get_by_id(self, run_id: str) -> Optional[Run]:
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
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Run]:
        """
        List runs with optional filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filtering terms

        Returns:
            List of Run objects

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError
