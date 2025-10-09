# Beacon Skeleton Implementation Guide

This guide walks you through implementing your own Beacon v2 API using this skeleton.

## Overview

The Beacon Skeleton provides:
1. **Complete API structure** - All Beacon v2 endpoints are defined
2. **Abstract service interfaces** - Contract for data access layer
3. **Pydantic models** - Type-safe request/response models
4. **Configuration management** - Environment-based settings

## Implementation Steps

### Step 1: Choose Your Database

First, decide on your database backend. Common choices:
- **PostgreSQL** - Recommended for production
- **MongoDB** - Good for flexible schemas
- **SQLite** - Good for development/testing
- **Custom API** - Wrap existing data sources

### Step 2: Install Database Dependencies

Add your database driver to `pyproject.toml`:

```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.5.0",
    "python-dotenv>=1.0.0",
    # Add your database driver
    "asyncpg>=0.29.0",  # For PostgreSQL
    # or
    "motor>=3.3.0",     # For MongoDB
    # or
    "aiosqlite>=0.19.0", # For SQLite
]
```

### Step 3: Create Database Connection Manager

Create `src/beacon_api/db/connection.py`:

```python
"""Database connection management."""

from typing import AsyncGenerator
from contextlib import asynccontextmanager
import asyncpg  # or your database driver

from beacon_api.core.config import get_settings


class Database:
    """Database connection manager."""

    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        """Create database connection pool."""
        settings = get_settings()
        self.pool = await asyncpg.create_pool(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password.get_secret_value(),
            database=settings.db_name,
            min_size=settings.db_pool_min_size,
            max_size=settings.db_pool_max_size,
        )

    async def disconnect(self) -> None:
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get a database connection from the pool."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            yield conn


# Global database instance
database = Database()
```

### Step 4: Implement Service Classes

Create `src/beacon_api/services/implementations.py`:

```python
"""Concrete service implementations."""

from typing import Optional
from beacon_api.services.base import IndividualService, BiosampleService
from beacon_api.models.entities import Individual, Biosample
from beacon_api.models.request import BeaconRequestBody, FilteringTerm
from beacon_api.db.connection import database


class PostgresIndividualService(IndividualService):
    """PostgreSQL implementation of IndividualService."""

    async def get_by_id(self, individual_id: str) -> Optional[Individual]:
        """Retrieve an individual by ID."""
        async with database.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM individuals WHERE id = $1",
                individual_id
            )
            if row:
                return Individual(**dict(row))
            return None

    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Individual]:
        """List individuals with pagination and filtering."""
        query = "SELECT * FROM individuals"
        params = []

        # Apply filters if provided
        if filters:
            conditions = []
            for i, filter_term in enumerate(filters, start=1):
                # Build filter conditions based on your schema
                # This is a simplified example
                conditions.append(f"filter_column = ${i}")
                params.append(filter_term.value)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        query += f" OFFSET ${len(params) + 1} LIMIT ${len(params) + 2}"
        params.extend([skip, limit])

        async with database.connection() as conn:
            rows = await conn.fetch(query, *params)
            return [Individual(**dict(row)) for row in rows]

    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Individual]:
        """Query individuals based on Beacon request."""
        # Build complex query from request_body
        conditions = []
        params = []

        # Add filters
        if request_body.filters:
            for i, filter_term in enumerate(request_body.filters):
                # Example: handle ontology filters
                if filter_term.type == "ontology":
                    conditions.append(f"phenotypes @> ${i + 1}")
                    params.append([filter_term.id])

        query = "SELECT * FROM individuals"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Apply pagination from request
        pagination = request_body.meta.pagination or {}
        skip = pagination.get("skip", 0)
        limit = pagination.get("limit", 10)
        query += f" OFFSET ${len(params) + 1} LIMIT ${len(params) + 2}"
        params.extend([skip, limit])

        async with database.connection() as conn:
            rows = await conn.fetch(query, *params)
            return [Individual(**dict(row)) for row in rows]


class PostgresBiosampleService(BiosampleService):
    """PostgreSQL implementation of BiosampleService."""

    async def get_by_id(self, biosample_id: str) -> Optional[Biosample]:
        """Retrieve a biosample by ID."""
        async with database.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM biosamples WHERE id = $1",
                biosample_id
            )
            if row:
                return Biosample(**dict(row))
            return None

    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Biosample]:
        """List biosamples with pagination."""
        query = "SELECT * FROM biosamples OFFSET $1 LIMIT $2"
        async with database.connection() as conn:
            rows = await conn.fetch(query, skip, limit)
            return [Biosample(**dict(row)) for row in rows]

    async def query(
        self,
        request_body: BeaconRequestBody,
    ) -> list[Biosample]:
        """Query biosamples based on Beacon request."""
        # Similar to IndividualService implementation
        pass


# Implement other services similarly:
# - PostgresGenomicVariationService
# - PostgresAnalysisService
# - PostgresCohortService
# - PostgresDatasetService
# - PostgresRunService
```

### Step 5: Update Dependencies

Update `src/beacon_api/api/dependencies.py`:

```python
"""Dependency injection for services."""

from typing import Annotated
from fastapi import Depends

from beacon_api.services.base import (
    IndividualService,
    BiosampleService,
    # ... other services
)
from beacon_api.services.implementations import (
    PostgresIndividualService,
    PostgresBiosampleService,
    # ... other implementations
)


def get_individual_service() -> IndividualService:
    """Get IndividualService implementation."""
    return PostgresIndividualService()


def get_biosample_service() -> BiosampleService:
    """Get BiosampleService implementation."""
    return PostgresBiosampleService()


# Update type aliases
IndividualServiceDep = Annotated[
    IndividualService,
    Depends(get_individual_service)
]
BiosampleServiceDep = Annotated[
    BiosampleService,
    Depends(get_biosample_service)
]
# ... other dependencies
```

### Step 6: Update Application Lifespan

Update `src/beacon_api/main.py`:

```python
from beacon_api.db.connection import database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    # Startup
    await database.connect()
    logger.info("Database connected")

    yield

    # Shutdown
    await database.disconnect()
    logger.info("Database disconnected")
```

### Step 7: Add Database Configuration

Update `src/beacon_api/core/config.py`:

```python
from pydantic import SecretStr

class Settings(BaseSettings):
    # ... existing settings ...

    # Database Configuration
    db_host: str = Field(default="localhost", description="Database host")
    db_port: int = Field(default=5432, description="Database port")
    db_user: str = Field(default="beacon", description="Database user")
    db_password: SecretStr = Field(description="Database password")
    db_name: str = Field(default="beacon", description="Database name")
    db_pool_min_size: int = Field(default=5, description="Min pool size")
    db_pool_max_size: int = Field(default=20, description="Max pool size")
```

### Step 8: Create Database Schema

Create migration scripts or SQL files for your database schema:

```sql
-- migrations/001_initial_schema.sql

CREATE TABLE individuals (
    id VARCHAR(255) PRIMARY KEY,
    sex VARCHAR(50),
    ethnicity JSONB,
    geographic_origin JSONB,
    diseases JSONB,
    phenotypic_features JSONB,
    interventions_or_procedures JSONB,
    measures JSONB,
    info JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE biosamples (
    id VARCHAR(255) PRIMARY KEY,
    individual_id VARCHAR(255) REFERENCES individuals(id),
    biosample_status JSONB,
    sample_origin_type JSONB,
    sample_origin_detail JSONB,
    collection_date VARCHAR(50),
    collection_moment VARCHAR(255),
    obtained_from_id VARCHAR(255),
    phenotypic_features JSONB,
    measurements JSONB,
    pathological_stage JSONB,
    tumor_progression JSONB,
    tumor_grade JSONB,
    diagnostic_markers JSONB,
    procedure JSONB,
    info JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes for common queries
CREATE INDEX idx_individuals_sex ON individuals(sex);
CREATE INDEX idx_individuals_phenotypes ON individuals USING GIN(phenotypic_features);
CREATE INDEX idx_biosamples_individual ON biosamples(individual_id);

-- Continue with other tables...
```

### Step 9: Add Tests for Your Implementation

Create `tests/test_services.py`:

```python
"""Tests for service implementations."""

import pytest
from beacon_api.services.implementations import PostgresIndividualService
from beacon_api.models.request import BeaconRequestBody


@pytest.fixture
async def individual_service():
    """Create individual service instance."""
    # Setup test database connection
    service = PostgresIndividualService()
    yield service
    # Cleanup


@pytest.mark.asyncio
async def test_get_individual_by_id(individual_service):
    """Test retrieving individual by ID."""
    individual = await individual_service.get_by_id("IND001")
    assert individual is not None
    assert individual.id == "IND001"


@pytest.mark.asyncio
async def test_list_individuals(individual_service):
    """Test listing individuals with pagination."""
    individuals = await individual_service.list(skip=0, limit=10)
    assert isinstance(individuals, list)
    assert len(individuals) <= 10
```

## Best Practices

### 1. Error Handling

Implement proper error handling in your services:

```python
from fastapi import HTTPException

async def get_by_id(self, individual_id: str) -> Optional[Individual]:
    try:
        async with database.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM individuals WHERE id = $1",
                individual_id
            )
            if row:
                return Individual(**dict(row))
            return None
    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

### 2. Caching

Consider adding caching for frequently accessed data:

```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@cache(expire=300)  # 5 minutes
async def get_by_id(self, individual_id: str) -> Optional[Individual]:
    # Implementation
    pass
```

### 3. Logging

Add structured logging:

```python
import logging
from beacon_api.core.config import get_settings

logger = logging.getLogger(__name__)

async def query(self, request_body: BeaconRequestBody) -> list[Individual]:
    logger.info(
        "Querying individuals",
        extra={
            "filters": len(request_body.filters or []),
            "granularity": request_body.meta.requested_granularity,
        }
    )
    # Implementation
```

### 4. Performance Optimization

- Use database indexes for common query patterns
- Implement connection pooling
- Consider read replicas for heavy read workloads
- Add query result caching

## Testing Your Implementation

1. **Unit tests** - Test individual service methods
2. **Integration tests** - Test API endpoints with real database
3. **Load tests** - Test performance under load
4. **Security tests** - Test authentication and authorization

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Health checks passing
- [ ] Monitoring and logging configured
- [ ] Rate limiting implemented (if needed)
- [ ] Authentication/authorization implemented
- [ ] CORS properly configured
- [ ] SSL/TLS certificates configured
- [ ] Backup strategy in place

## Additional Resources

- [Beacon v2 Documentation](https://docs.genomebeacons.org/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
