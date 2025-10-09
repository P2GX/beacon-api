# Quick Start Guide

Get your Beacon v2 API up and running in minutes!

## Prerequisites

- Python 3.11+ installed
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

## Installation Steps

### 1. Install Dependencies

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings (optional for testing)
# The defaults will work out of the box
```

### 3. Run the Development Server

```bash
# Start the server
uvicorn beacon_api.main:app --reload

# Or use the Python module directly
python -m beacon_api.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Beacon Info**: http://localhost:8000/api/info

## Test the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Get Beacon info
curl http://localhost:8000/api/info

# Query individuals (will return 501 until you implement services)
curl -X POST http://localhost:8000/api/individuals \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "requested_granularity": "boolean"
    }
  }'
```

### Using the Interactive Docs

1. Open http://localhost:8000/docs in your browser
2. Browse available endpoints
3. Click "Try it out" on any endpoint
4. Execute requests directly from the browser

## Next Steps

The skeleton is now running, but endpoints will return 501 (Not Implemented) until you add your database implementation.

### Implement Your Database Backend

1. **Choose a database** (PostgreSQL, MongoDB, SQLite, etc.)
2. **Install database driver**:
   ```bash
   # For PostgreSQL
   uv pip install asyncpg

   # For MongoDB
   uv pip install motor

   # For SQLite
   uv pip install aiosqlite
   ```

3. **Create service implementations**:
   - See `docs/implementation_guide.md` for detailed instructions
   - Implement abstract methods from `src/beacon_api/services/base.py`
   - Update `src/beacon_api/api/dependencies.py` with your implementations

4. **Set up your database**:
   - Create database schema
   - Add migration scripts
   - Configure connection in `.env`

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/beacon_api --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
# xdg-open htmlcov/index.html  # On Linux
# start htmlcov/index.html  # On Windows
```

### Docker Deployment

```bash
# Build image
docker build -t beacon-api:latest .

# Run container
docker run -p 8000:8000 beacon-api:latest

# Test health check
curl http://localhost:8000/health
```

## Project Structure Overview

```
beacon-api/
├── src/beacon_api/
│   ├── api/              # FastAPI routers
│   ├── models/           # Pydantic models
│   ├── services/         # Service interfaces (implement these!)
│   ├── core/             # Configuration
│   └── main.py           # Application entry point
├── tests/                # Test suite
├── docs/                 # Documentation
└── pyproject.toml        # Dependencies
```

## Common Issues

### Port Already in Use
```bash
# Use a different port
uvicorn beacon_api.main:app --reload --port 8001
```

### Import Errors
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall in editable mode
uv pip install -e .
```

### Dependencies Not Found
```bash
# Reinstall all dependencies
uv pip install -e ".[dev]"
```

## Getting Help

- Read the full [README.md](README.md)
- Check the [Implementation Guide](docs/implementation_guide.md)
- Review the [Beacon v2 Specification](https://docs.genomebeacons.org/)
- Open an issue on GitHub

## What's Included

✅ Complete Beacon v2 API structure
✅ All standard endpoints (individuals, biosamples, genomic variations, etc.)
✅ Request/response validation with Pydantic
✅ Configuration management
✅ Docker support
✅ GitHub Actions CI/CD
✅ Test framework
✅ Comprehensive documentation

**What You Need to Add**: Your database implementation!

---

Ready to implement? Start with `docs/implementation_guide.md`!
