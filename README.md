# Beacon API

A production-ready implementation of the [GA4GH Beacon v2 API](https://github.com/ga4gh-beacon/beacon-v2) using FastAPI. This project provides a complete, idiomatic FastAPI structure with abstract service interfaces, making it easy to implement your own database backend.

## Features

- ✅ **Complete Beacon v2 API implementation** with all standard endpoints
- ✅ **Clean architecture** with separation of concerns (models, services, API)
- ✅ **Abstract service interfaces** - plug in your own database implementation
- ✅ **Type-safe** with full Pydantic models and type hints
- ✅ **Production-ready** with Docker support and health checks
- ✅ **CI/CD** with GitHub Actions (linting, testing, Docker builds)
- ✅ **Configuration** using Pydantic Settings with environment variables
- ✅ **Modern tooling** - uv, ruff, mypy

## Architecture

```
beacon-api/
├── src/beacon_api/
│   ├── api/                    # FastAPI routers and endpoints
│   │   ├── individuals.py      # Individuals endpoint
│   │   ├── biosamples.py       # Biosamples endpoint
│   │   ├── genomic_variations.py
│   │   ├── analyses.py
│   │   ├── cohorts.py
│   │   ├── datasets.py
│   │   ├── runs.py
│   │   ├── info.py             # Beacon info endpoint
│   │   └── dependencies.py     # Dependency injection
│   ├── models/                 # Pydantic models
│   │   ├── common.py           # Shared models
│   │   ├── request.py          # Request models
│   │   ├── response.py         # Response models
│   │   └── entities.py         # Entity models
│   ├── services/               # Service layer (interfaces)
│   │   └── base.py             # Abstract base classes
│   ├── core/                   # Core application logic
│   │   └── config.py           # Configuration management
│   └── main.py                 # FastAPI application
├── tests/                      # Test suite
├── Dockerfile                  # Docker configuration
├── pyproject.toml              # Project metadata and dependencies
└── .github/workflows/          # CI/CD pipelines
```

## Quick Start

### Prerequisites

- Python 3.11 or 3.12
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/beacon-api.git
cd beacon-api
```

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

3. Copy the example environment file and customize:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the development server:
```bash
uvicorn beacon_api.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Implementing Your Database

The skeleton provides abstract service interfaces that you need to implement for your database backend. Here's how:

### 1. Create Your Service Implementation

Create a new file `src/beacon_api/services/implementations.py`:

```python
from typing import Optional
from beacon_api.services.base import IndividualService
from beacon_api.models.entities import Individual
from beacon_api.models.request import BeaconRequestBody, FilteringTerm

class MyIndividualService(IndividualService):
    def __init__(self, db_connection):
        self.db = db_connection

    async def get_by_id(self, individual_id: str) -> Optional[Individual]:
        # Query your database
        result = await self.db.query(
            "SELECT * FROM individuals WHERE id = ?", individual_id
        )
        if result:
            return Individual(**result)
        return None

    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[list[FilteringTerm]] = None,
    ) -> list[Individual]:
        # Implement your pagination and filtering logic
        results = await self.db.query(
            "SELECT * FROM individuals LIMIT ? OFFSET ?", limit, skip
        )
        return [Individual(**r) for r in results]

    async def query(self, request_body: BeaconRequestBody) -> list[Individual]:
        # Implement complex query logic based on request_body
        pass

# Implement similar classes for other entities:
# - MyBiosampleService
# - MyGenomicVariationService
# - MyAnalysisService
# - MyCohortService
# - MyDatasetService
# - MyRunService
```

### 2. Override Dependencies

Update `src/beacon_api/api/dependencies.py`:

```python
from beacon_api.services.implementations import MyIndividualService
from your_database import get_db_connection

def get_individual_service() -> IndividualService:
    db = get_db_connection()
    return MyIndividualService(db)

# Override other service dependencies similarly
```

### 3. Initialize Database in Lifespan

Update `src/beacon_api/main.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: Initialize your database
    await database.connect()
    yield
    # Shutdown: Cleanup
    await database.disconnect()
```

## Configuration

All configuration is managed through environment variables using Pydantic Settings. See `.env.example` for available options.

Key configuration categories:
- **API Configuration**: Version, environment
- **Beacon Information**: ID, name, description, URLs
- **Organization Information**: Name, contact details
- **Server Configuration**: Host, port, logging
- **CORS Configuration**: Allowed origins, methods, headers

## Docker Deployment

### Build the Docker image:
```bash
docker build -t beacon-api:latest .
```

### Run the container:
```bash
docker run -p 8000:8000 \
  -e BEACON_ID=my.beacon \
  -e BEACON_NAME="My Beacon" \
  beacon-api:latest
```

### Using Docker Compose:
```yaml
version: '3.8'
services:
  beacon:
    build: .
    ports:
      - "8000:8000"
    environment:
      - BEACON_ID=my.beacon
      - BEACON_NAME=My Beacon
      - ENVIRONMENT=production
    env_file:
      - .env
```

## Development

### Code Quality

Format code with ruff:
```bash
ruff format src/ tests/
```

Lint with ruff:
```bash
ruff check src/ tests/
```

Type check with mypy:
```bash
mypy src/
```

### Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=src/beacon_api --cov-report=html
```

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

## API Endpoints

### Info
- `GET /api/info` - Get Beacon information

### Individuals
- `GET /api/individuals` - List all individuals
- `GET /api/individuals/{id}` - Get individual by ID
- `POST /api/individuals` - Query individuals with filters

### Biosamples
- `GET /api/biosamples` - List all biosamples
- `GET /api/biosamples/{id}` - Get biosample by ID
- `POST /api/biosamples` - Query biosamples with filters

### Genomic Variations
- `GET /api/g_variants` - List all genomic variations
- `GET /api/g_variants/{id}` - Get genomic variation by ID
- `POST /api/g_variants` - Query genomic variations

### Other Entities
- Analyses: `/api/analyses`
- Cohorts: `/api/cohorts`
- Datasets: `/api/datasets`
- Runs: `/api/runs`

### Query Granularity

All POST endpoints support different response granularities:
- `boolean`: Returns only whether matches exist
- `count`: Returns count of matches
- `record`: Returns full matching records

Example query:
```json
{
  "meta": {
    "requested_granularity": "count"
  },
  "query": {
    "assembly_id": "GRCh38",
    "reference_name": "1",
    "start": [100000],
    "end": [200000]
  },
  "filters": [
    {
      "type": "ontology",
      "id": "HP:0001250",
      "scope": "individuals"
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Apache License 2.0

## Resources

- [GA4GH Beacon v2 Specification](https://docs.genomebeacons.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Support

For questions or issues, please open an issue on GitHub.

---

**Note**: This is a skeleton implementation with abstract service interfaces. You must implement the service layer for your specific database backend before deploying to production.
