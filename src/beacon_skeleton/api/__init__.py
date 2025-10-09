"""FastAPI routers for Beacon v2 API endpoints."""

from beacon_skeleton.api.info import router as info_router
from beacon_skeleton.api.individuals import router as individuals_router
from beacon_skeleton.api.biosamples import router as biosamples_router
from beacon_skeleton.api.genomic_variations import router as g_variations_router
from beacon_skeleton.api.analyses import router as analyses_router
from beacon_skeleton.api.cohorts import router as cohorts_router
from beacon_skeleton.api.datasets import router as datasets_router
from beacon_skeleton.api.runs import router as runs_router

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
