# Integration Tests

This directory contains integration tests for the Banking API that test the complete functionality of the system, including interactions between components and external dependencies.

## Test Files

### `test_rest_api.py`
- **Purpose**: Tests REST API endpoints end-to-end
- **Coverage**: Account creation, retrieval, transactions, error handling
- **Requirements**: Banking API server running on `http://localhost:8000`
- **Type**: Direct HTTP requests using `requests` library

### `test_websocket.py`
- **Purpose**: Tests WebSocket functionality for real-time updates
- **Coverage**: WebSocket connections, transaction broadcasting, stats endpoints
- **Requirements**: Banking API server with WebSocket support
- **Type**: Async WebSocket testing using `websockets` and `pytest`

## Running the Tests

### Prerequisites
1. Start the Banking API server:
   ```bash
   cd .. # Go back to banking-api root
   python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

2. Ensure dependencies are installed:
   ```bash
   cd .. # Go back to banking-api root
   pip install -r api/requirements.txt
   pip install -r requirements-dev.txt
   ```

### Running Individual Tests

```bash
# REST API integration tests
python test_rest_api.py

# WebSocket integration tests  
pytest test_websocket.py -v

# Run all integration tests
python test_rest_api.py && pytest test_websocket.py -v
```

### Running with Pytest

```bash
# Run all tests in this directory
pytest -v

# Run with coverage
pytest --cov=.. --cov-report=html -v

# Run specific test classes
pytest test_websocket.py::TestWebSocketIntegration -v
```

## Test Structure

### REST API Tests (`test_rest_api.py`)
- Account creation and validation
- Transaction processing
- Balance updates
- Error scenarios
- Data consistency checks

### WebSocket Tests (`test_websocket.py`)
- Connection establishment
- Real-time transaction broadcasts
- Multiple client connections
- WebSocket statistics
- Error handling and reconnection

## CI/CD Integration

These tests are automatically run in the CI pipeline:

1. **Unit Tests Phase**: Domain and business logic tests
2. **Integration Tests Phase**: 
   - REST API tests (`test_rest_api.py`)
   - WebSocket tests (`test_websocket.py`)
3. **End-to-End Tests**: Full system validation

## Debugging Integration Tests

### REST API Tests
- Check server logs for API request/response details
- Verify database state after operations
- Use HTTP debugging tools like curl or Postman

### WebSocket Tests  
- Enable WebSocket debugging in the server
- Check connection logs and message flow
- Use browser dev tools for WebSocket inspection

## Adding New Integration Tests

1. **For REST API**: Add functions to `test_rest_api.py`
2. **For WebSocket**: Add test methods to `TestWebSocketIntegration` class
3. **For new features**: Create new test files following the naming pattern `test_*.py`

## Best Practices

- **Isolation**: Each test should be independent and clean up after itself
- **Data**: Use test-specific data that doesn't conflict with other tests
- **Timing**: Include appropriate waits for async operations
- **Assertions**: Use clear, descriptive assertions
- **Error Cases**: Test both success and failure scenarios
