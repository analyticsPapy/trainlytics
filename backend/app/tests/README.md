# Trainlytics - Tests

This directory contains unit tests and integration tests for the Trainlytics backend.

## Test Structure

```
tests/
├── __init__.py
├── test_api/
│   ├── __init__.py
│   └── test_auth.py          # Authentication endpoint tests
├── test_connectors/
│   ├── __init__.py
│   └── test_strava_connector.py  # Strava connector tests
└── README.md
```

## Running Tests

### Run All Tests

```bash
cd backend
pytest
```

### Run Specific Test File

```bash
pytest app/tests/test_api/test_auth.py
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test Function

```bash
pytest app/tests/test_connectors/test_strava_connector.py::TestStravaConnector::test_get_authorization_url
```

## Test Categories

### 1. Connector Tests

Tests for external API connectors (Strava, Garmin, Polar, Coros):

- OAuth flow (authorization, token exchange, refresh)
- Activity fetching and normalization
- Webhook handling
- Error handling and rate limiting

**Example:**
```bash
pytest app/tests/test_connectors/
```

### 2. API Tests

Tests for FastAPI endpoints:

- Authentication (login, register, token validation)
- User management
- Activity CRUD operations
- Workout management

**Example:**
```bash
pytest app/tests/test_api/
```

### 3. Service Tests

Tests for business logic services (coming soon):

- Activity synchronization
- Metrics calculation
- Permissions and coach-athlete relationships

## Writing Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test<ComponentName>`
- Test functions: `test_<what_it_tests>`

### Example Test

```python
import pytest
from unittest.mock import AsyncMock, patch

class TestExampleFeature:
    """Test suite for example feature."""

    @pytest.fixture
    def mock_data(self):
        """Provide test data."""
        return {'id': 1, 'name': 'Test'}

    @pytest.mark.asyncio
    async def test_async_function(self, mock_data):
        """Test async function."""
        with patch('app.some_module.func', new_callable=AsyncMock) as mock_func:
            mock_func.return_value = mock_data

            result = await some_async_function()

            assert result['id'] == 1
            mock_func.assert_called_once()
```

## Fixtures

Common fixtures are defined in `conftest.py`:

```python
@pytest.fixture
async def prisma_client():
    """Provide Prisma client for tests."""
    client = Prisma()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.fixture
def test_user():
    """Provide test user data."""
    return {
        'email': 'test@example.com',
        'password': 'test_password_123',
        'name': 'Test User'
    }
```

## Mocking External APIs

Always mock external API calls in tests:

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_strava_api_call():
    with patch.object(connector.client, 'get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {'data': 'test'}
        )

        result = await connector.get_data()

        assert result == {'data': 'test'}
```

## Testing Best Practices

### ✅ Do's

- Write tests for all new features
- Mock external dependencies
- Use descriptive test names
- Test both success and failure cases
- Keep tests isolated and independent
- Use fixtures for common test data

### ❌ Don'ts

- Don't make real API calls to external services
- Don't rely on test execution order
- Don't share state between tests
- Don't skip writing tests for "simple" functions
- Don't commit commented-out tests

## Continuous Integration

Tests are automatically run on:

- Every pull request
- Every push to main branch
- Before deployment

## Coverage Goals

We aim for:

- **Overall coverage**: > 80%
- **Critical paths**: 100% (auth, connectors, data sync)
- **API endpoints**: > 90%

## Debugging Tests

### Run with pdb

```bash
pytest --pdb
```

Drops into debugger on first failure.

### Print Statements

```python
def test_something():
    result = function_under_test()
    print(f"Result: {result}")  # Will be captured by pytest
    assert result == expected
```

View captured output:
```bash
pytest -s  # Don't capture output
```

## Test Data

Test data should be:

- **Realistic**: Similar to production data
- **Minimal**: Only what's needed for the test
- **Isolated**: Not dependent on other tests
- **Clean**: Clear and readable

## Troubleshooting

### Issue: "Module not found"

**Solution**: Ensure you're running from the backend directory:
```bash
cd backend
pytest
```

### Issue: "Async tests not running"

**Solution**: Install pytest-asyncio:
```bash
pip install pytest-asyncio
```

### Issue: "Database connection error"

**Solution**: Use test database URL in `.env.test`:
```bash
DATABASE_URL="postgresql://postgres:password@localhost:5432/trainlytics_test"
```

## Contributing

When adding new features:

1. Write tests first (TDD approach recommended)
2. Ensure all tests pass
3. Check coverage hasn't decreased
4. Update this README if adding new test categories

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
