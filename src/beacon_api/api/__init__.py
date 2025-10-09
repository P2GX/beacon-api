"""FastAPI routers for Beacon v2 API endpoints."""

from beacon_api.api.info import router as info_router
from beacon_api.api.individuals import router as individuals_router
from beacon_api.api.biosamples import router as biosamples_router
from beacon_api.api.genomic_variations import router as g_variations_router
from beacon_api.api.analyses import router as analyses_router
from beacon_api.api.cohorts import router as cohorts_router
from beacon_api.api.datasets import router as datasets_router
from beacon_api.api.runs import router as runs_router

__all__ = [
    "info_router",
    "individuals_router",
    "biosamples_router",
    "g_variations_router",
    "analyses_router",
    "cohorts_router",
    "datasets_router",
    "runs_router",
]
