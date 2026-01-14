"""Stub service implementations for Beacon API.

These implementations allow the API to start and respond to requests
without a backend implementation, which is useful for beacon-verifier
compliance and development/testing.

All methods raise NotImplementedError when called, which the endpoint
handlers catch and convert to appropriate empty responses.
"""

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
from beacon_api.services.base import (
    AnalysisService,
    BiosampleService,
    CohortService,
    DatasetService,
    GenomicVariationService,
    IndividualService,
    RunService,
)


class StubIndividualService(IndividualService):
    """Stub implementation of IndividualService."""

    async def get_by_id(self, individual_id: str) -> Individual | None:
        """Get individual by ID - not implemented."""
        raise NotImplementedError("IndividualService not implemented")

    async def query(self, request_body: BeaconRequestBody) -> list[Individual]:
        """Query individuals - not implemented."""
        raise NotImplementedError("IndividualService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count individuals - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if individuals exist - returns False."""
        return False


class StubBiosampleService(BiosampleService):
    """Stub implementation of BiosampleService."""

    async def get_by_id(self, biosample_id: str) -> Biosample | None:
        """Get biosample by ID - not implemented."""
        raise NotImplementedError("BiosampleService not implemented")

    async def query(self, request_body: BeaconRequestBody) -> list[Biosample]:
        """Query biosamples - not implemented."""
        raise NotImplementedError("BiosampleService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count biosamples - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if biosamples exist - returns False."""
        return False


class StubGenomicVariationService(GenomicVariationService):
    """Stub implementation of GenomicVariationService."""

    async def get_by_id(self, variation_id: str) -> GenomicVariation | None:
        """Get genomic variation by ID - not implemented."""
        raise NotImplementedError("GenomicVariationService not implemented")

    async def query(
        self, request_body: BeaconRequestBody
    ) -> list[GenomicVariation]:
        """Query genomic variations - not implemented."""
        raise NotImplementedError("GenomicVariationService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count genomic variations - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if genomic variations exist - returns False."""
        return False


class StubAnalysisService(AnalysisService):
    """Stub implementation of AnalysisService."""

    async def get_by_id(self, analysis_id: str) -> Analysis | None:
        """Get analysis by ID - not implemented."""
        raise NotImplementedError("AnalysisService not implemented")

    async def query(self, request_body: BeaconRequestBody) -> list[Analysis]:
        """Query analyses - not implemented."""
        raise NotImplementedError("AnalysisService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count analyses - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if analyses exist - returns False."""
        return False


class StubCohortService(CohortService):
    """Stub implementation of CohortService."""

    async def get_by_id(self, cohort_id: str) -> Cohort | None:
        """Get cohort by ID - not implemented."""
        raise NotImplementedError("CohortService not implemented")

    async def query(self, request_body: BeaconRequestBody) -> list[Cohort]:
        """Query cohorts - not implemented."""
        raise NotImplementedError("CohortService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count cohorts - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if cohorts exist - returns False."""
        return False


class StubDatasetService(DatasetService):
    """Stub implementation of DatasetService."""

    async def get_by_id(self, dataset_id: str) -> Dataset | None:
        """Get dataset by ID - not implemented."""
        raise NotImplementedError("DatasetService not implemented")

    async def query(self, request_body: BeaconRequestBody) -> list[Dataset]:
        """Query datasets - not implemented."""
        raise NotImplementedError("DatasetService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count datasets - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if datasets exist - returns False."""
        return False


class StubRunService(RunService):
    """Stub implementation of RunService."""

    async def get_by_id(self, run_id: str) -> Run | None:
        """Get run by ID - not implemented."""
        raise NotImplementedError("RunService not implemented")

    async def query(self, request_body: BeaconRequestBody) -> list[Run]:
        """Query runs - not implemented."""
        raise NotImplementedError("RunService not implemented")

    async def count(self, request_body: BeaconRequestBody) -> int:
        """Count runs - returns 0."""
        return 0

    async def exists(self, request_body: BeaconRequestBody) -> bool:
        """Check if runs exist - returns False."""
        return False
