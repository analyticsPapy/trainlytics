# Trainlytics Backend

FastAPI backend for the Trainlytics training platform.

## Quick Start

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### With Docker

```bash
cd ..
docker-compose up backend
```

## API Documentation

When running locally, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Testing

```bash
pytest
pytest --cov=app tests/
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configuration
│   ├── db/           # Database setup
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── main.py       # FastAPI application
├── alembic/          # Database migrations
└── tests/            # Test files
```
