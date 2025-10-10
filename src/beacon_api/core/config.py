"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_version: str = Field(default="v2.0", description="Beacon API version")
    environment: str = Field(
        default="development",
        description="Environment: production, development, or staging",
    )

    # Beacon Information
    beacon_id: str = Field(
        default="org.example.beacon",
        description="Unique identifier for this Beacon",
    )
    beacon_name: str = Field(
        default="Beacon Skeleton",
        description="Human-readable name for this Beacon",
    )
    beacon_description: str | None = Field(
        default="A skeleton implementation of the GA4GH Beacon v2 API",
        description="Description of this Beacon",
    )
    beacon_version: str | None = Field(
        default="0.1.0",
        description="Version of this Beacon implementation",
    )
    beacon_welcome_url: str | None = Field(
        default=None,
        description="Welcome page URL",
    )
    beacon_alternative_url: str | None = Field(
        default=None,
        description="Alternative URL for this Beacon",
    )
    beacon_create_date_time: str | None = Field(
        default=None,
        description="Beacon creation date and time (ISO 8601 format)",
    )
    beacon_update_date_time: str | None = Field(
        default=None,
        description="Beacon last update date and time (ISO 8601 format)",
    )

    # Organization Information
    organization_id: str = Field(
        default="org.example",
        description="Organization identifier",
    )
    organization_name: str = Field(
        default="Example Organization",
        description="Organization name",
    )
    organization_description: str | None = Field(
        default="An example organization running a Beacon",
        description="Organization description",
    )
    organization_address: str | None = Field(
        default=None,
        description="Organization address",
    )
    organization_welcome_url: str | None = Field(
        default=None,
        description="Organization welcome page URL",
    )
    organization_contact_url: str | None = Field(
        default=None,
        description="Organization contact information URL",
    )
    organization_logo_url: str | None = Field(
        default=None,
        description="Organization logo URL",
    )

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    reload: bool = Field(
        default=False,
        description="Enable auto-reload for development",
    )
    log_level: str = Field(
        default="info",
        description="Logging level",
    )

    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["*"],
        description="List of allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(
        default=True,
        description="Allow credentials in CORS requests",
    )
    cors_allow_methods: list[str] = Field(
        default=["*"],
        description="Allowed HTTP methods for CORS",
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
        description="Allowed headers for CORS",
    )

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings (cached).

    Returns:
        Settings instance
    """
    return Settings()
