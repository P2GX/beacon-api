"""Monitor endpoint.

Provides health information about the Beacon service.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/monitor", tags=["monitor"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns a simple status message indicating the service is operational.

    Returns:
        A dictionary with a status message.
    """
    return {"status": "ok"}
