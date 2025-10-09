"""FastAPI routers for Beacon v2 API endpoints."""

from fast_beacon.api.info import router as info_router
from fast_beacon.api.individuals import router as individuals_router
from fast_beacon.api.biosamples import router as biosamples_router
from fast_beacon.api.genomic_variations import router as g_variations_router
from fast_beacon.api.analyses import router as analyses_router
from fast_beacon.api.cohorts import router as cohorts_router
from fast_beacon.api.datasets import router as datasets_router
from fast_beacon.api.runs import router as runs_router

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
