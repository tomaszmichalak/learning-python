# Contributing to Banking API

This document provides comprehensive guidelines for developing, debugging, testing, and deploying the Banking API module.

## 🏗️ Architecture Overview

The project follows a **Package-by-Feature** approach with domain-driven design:

- **Presentation Layer** (`api/main.py`): FastAPI endpoints that handle HTTP requests and responses
- **Domain Layer** (`api/domains/`): Business domains organized by feature
  - **Account Domain** (`api/domains/account/`): All account-related functionality
  - **Transaction Domain** (`api/domains/transaction/`): All transaction-related functionality

### Package-by-Feature Benefits

1. **High Cohesion**: Related functionality is grouped together
2. **Easy Navigation**: Find all account-related code in one place
3. **Domain Isolation**: Clear boundaries between business domains
4. **Scalability**: Easy to add new domains or features
5. **Team Organization**: Teams can own specific domains

### Domain Architecture

Each domain follows a consistent structure:

- **`models.py`**: Pydantic models, domain entities, and DTOs
- **`repository.py`**: Abstract repository interface
- **`memory_repository.py`**: Concrete repository implementation
- **`service.py`**: Business logic and domain operations

## 📁 Project Structure

```
banking-api/
├── api/                      # API layer
│   ├── main.py               # FastAPI application entry point
│   ├── start_server.py       # Server startup script
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   ├── Dockerfile            # Container configuration
│   ├── docker-compose.yml    # Docker Compose configuration
│   ├── test_domains.py       # Comprehensive domain tests
│   ├── services/             # Service layer implementations
│   │   ├── rest_service.py           # REST API service implementation
│   │   ├── websocket_service.py      # WebSocket service implementation
│   │   ├── websocket_manager.py      # WebSocket connection manager
│   │   └── debuggable_router.py      # Debug-friendly router implementation
│   └── domains/              # Domain-driven design modules (Package-by-Feature)
│       ├── __init__.py
│       ├── account/             # Account domain
│       │   ├── __init__.py
│       │   ├── models.py        # Account data models and DTOs
│       │   ├── service.py       # Account business logic
│       │   ├── repository.py    # Account data access interface
│       │   ├── memory_repository.py # In-memory account storage
│       │   └── test_account.py  # Account domain tests
│       └── transaction/         # Transaction domain
│           ├── __init__.py
│           ├── models.py        # Transaction data models and DTOs
│           ├── service.py       # Transaction business logic
│           ├── repository.py    # Transaction data access interface
│           ├── memory_repository.py # In-memory transaction storage
│           └── test_transaction.py # Transaction domain tests
├── it-tests/                # Integration tests
│   ├── test_rest_api.py     # REST API integration tests
│   └── test_websocket.py    # WebSocket integration tests
└── tools/                   # Development tools and utilities
    ├── debug_server.py      # Direct debugging script
    └── websocket_client_example.py # WebSocket testing client
```

## 🐛 Debugging Setup

### Prerequisites

1. **Python Virtual Environment**: Ensure you're using the project's virtual environment
   ```bash
   source /Users/tomaszmichalak/Projects/learning-python/.venv/bin/activate
   ```

2. **VS Code Extensions**: Install the Python extension for VS Code

### Debug Configurations

The project includes multiple VS Code debug configurations in `.vscode/launch.json`:

#### 🎯 Recommended: "Debug Banking API - No Reload"
- **Best for debugging**: Prevents auto-reload from interrupting debugging sessions
- **Usage**: Set breakpoints and press F5
- **Configuration**:
  ```json
  {
      "name": "Debug Banking API - No Reload",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["api.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"],
      "justMyCode": false,
      "reload": false
  }
  ```

#### "Debug Banking API - With Reload"
- **Good for development**: Auto-reloads on file changes
- **Note**: May interrupt debugging sessions

#### "Debug Banking API - Direct Script"
- **Alternative approach**: Uses `tools/debug_server.py` for maximum control
- **Usage**: For complex debugging scenarios

### Debugging Router Methods

#### Problem: Standard FastAPI Router Debugging Issues
FastAPI's dynamic routing and dependency injection can make it difficult for debuggers to step into router methods properly.

#### Solution: Debuggable Router
The project includes `api/services/debuggable_router.py` with class-based router methods that are easier to debug:

1. **Enable debuggable router** in `api/main.py`:
   ```python
   USE_DEBUGGABLE_ROUTER = True  # Set to True for debugging
   ```

2. **Set breakpoints** in `api/services/debuggable_router.py` methods:
   - `create_account()` - Account creation
   - `create_transaction()` - Transaction creation
   - `get_all_accounts()` - Account listing
   - Any other router method

3. **Debug workflow**:
   ```bash
   # Stop any running containers
   docker compose down banking-api
   
   # Start debugging in VS Code
   # Press F5 → Select "Debug Banking API - No Reload"
   
   # Test with curl in another terminal
   curl -X POST http://localhost:8000/api/accounts \
     -H "Content-Type: application/json" \
     -d '{"account_holder": "Debug Test", "account_type": "checking", "initial_balance": 1000}'
   ```

### Debug Features

#### Debug Logging
- **Level**: Set to `DEBUG` in debug mode
- **Location**: Console and VS Code Debug Console
- **Router methods**: Include debug print statements with 🐛 emoji

#### Key Debug Settings
- ✅ `justMyCode: false` - Allows stepping into FastAPI internals
- ✅ `reload: false` - Prevents reload issues during debugging
- ✅ `PYTHONPATH` set correctly
- ✅ Debug logging enabled
- ✅ Class-based router methods for clear breakpoint targets

## 🔧 Development Workflow

### Local Development

1. **Stop Docker containers** (if running):
   ```bash
   cd /Users/tomaszmichalak/Projects/learning-python/banking-compose
   docker compose down banking-api
   ```

2. **Navigate to banking-api directory**:
   ```bash
   cd /Users/tomaszmichalak/Projects/learning-python/banking-api
   ```

3. **Activate virtual environment**:
   ```bash
   source ../../../.venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r api/requirements.txt
   ```

5. **Start debugging or run directly**:
   ```bash
   # Option 1: Use VS Code debugger (RECOMMENDED)
   # Press F5 in VS Code
   
   # Option 2: Run directly with uvicorn
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   
   # Option 3: Use debug script
   python tools/debug_server.py
   ```

### Testing API Endpoints

#### Create Account
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"account_holder": "Test User", "account_type": "checking", "initial_balance": 1000}'
```

#### Create Transaction
```bash
# Save account ID from previous response
account_id="<ACCOUNT_ID_FROM_RESPONSE>"

curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d "{\"account_id\": \"$account_id\", \"amount\": 100, \"transaction_type\": \"deposit\", \"description\": \"Test transaction\"}"
```

#### Test WebSocket Connection
```bash
# Open in browser for real-time testing
open http://localhost:3000/websocket-direct-test.html
```

## 🐳 Docker Development

### Local Development Setup

#### Option 1: Local Python Environment (Recommended for Development)

1. **Stop Docker containers** (if running):
   ```bash
   cd /Users/tomaszmichalak/Projects/learning-python/banking-compose
   docker compose down banking-api
   ```

2. **Navigate to banking-api directory**:
   ```bash
   cd /Users/tomaszmichalak/Projects/learning-python/banking-api
   ```

3. **Activate virtual environment**:
   ```bash
   source ../../../.venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r api/requirements.txt
   ```

5. **Start debugging or run directly**:
   ```bash
   # Option 1: Use VS Code debugger (RECOMMENDED)
   # Press F5 in VS Code
   
   # Option 2: Run directly with uvicorn
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   
   # Option 3: Use debug script
   python tools/debug_server.py
   
   # Option 4: Use start server script
   python api/start_server.py
   ```

#### Option 2: Docker Development

1. **Navigate to api directory:**
   ```bash
   cd /Users/tomaszmichalak/Projects/learning-python/banking-api/api
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker compose up --build
   ```

3. **Or build and run with Docker directly:**
   ```bash
   # Build the image
   docker build -t banking-api .
   
   # Run the container
   docker run -d --name banking-api -p 8000:8000 banking-api
   ```

### Docker Commands Reference

#### Development with Docker Compose
```bash
# Navigate to api directory first
cd /Users/tomaszmichalak/Projects/learning-python/banking-api/api

# Start the application in development mode
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build banking-api

# Run tests in container
docker-compose run --rm banking-api pytest domains/ -v
```

#### Production Docker Commands
```bash
# Navigate to api directory
cd /Users/tomaszmichalak/Projects/learning-python/banking-api/api

# Build the production image
docker build -t banking-api:latest .

# Run the container
docker run -d \
  --name banking-api \
  --restart unless-stopped \
  -p 8000:8000 \
  banking-api:latest

# View container logs
docker logs -f banking-api

# Stop and remove container
docker stop banking-api && docker rm banking-api
```

### Development vs Production
- **Development**: Use VS Code debugger with local Python for best debugging experience
- **Production**: Use Docker Compose with `banking-api` service for deployment

## 🔒 Security Configuration

This project includes security best practices to address common security scan findings:

### Host Binding Configuration

The application uses secure host binding defaults:

- **Local Development**: Binds to `127.0.0.1` (localhost only) by default
- **Docker Containers**: Binds to `0.0.0.0` (required for container networking)
- **Production**: Configurable via environment variables

#### Environment Variables

```bash
# Set the host binding (default: 127.0.0.1 for local development)
export HOST=127.0.0.1       # Local development (secure default)
export HOST=0.0.0.0         # Docker/container environments
export PORT=8000            # Port number (default: 8000)
```

#### Usage Examples

```bash
# Local development (secure default)
python api/start_server.py
# Starts on 127.0.0.1:8000

# Allow external connections (if needed for development)
HOST=0.0.0.0 python api/start_server.py
# Starts on 0.0.0.0:8000

# Custom port
PORT=3000 python api/start_server.py
# Starts on 127.0.0.1:3000
```

#### Docker Environments

In Docker containers, `0.0.0.0` binding is automatically used and is safe within the container environment:

```dockerfile
# Dockerfile uses 0.0.0.0 binding (safe in containers)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]  # nosec B104
```

The `# nosec B104` comment tells security scanners that this usage is intentional and reviewed.

### Security Notes

- Never bind to `0.0.0.0` on production servers unless behind proper firewall/proxy
- Use environment variables for configuration instead of hardcoded values
- Container binding to `0.0.0.0` is safe within container networking
- Always review security scan findings and apply appropriate mitigations

## 🚀 WebSocket Deployment

### Docker Deployment
The WebSocket functionality works seamlessly with the existing Docker setup:
- No additional ports needed (uses same HTTP port)
- NGINX proxy supports WebSocket upgrades
- Health checks include WebSocket status

### Production Considerations
- Use a message queue (Redis, RabbitMQ) for multi-instance deployments
- Implement WebSocket authentication and authorization
- Add monitoring for WebSocket connection health
- Consider connection limits and resource management
- Monitor connection statistics and performance

### Monitoring WebSocket Health

```bash
# Check WebSocket connection statistics
curl http://localhost:8000/api/ws/stats

# Monitor in production
curl https://your-domain.com/api/ws/stats

# Example response
{
  "total_connections": 15,
  "global_connections": 3,
  "account_connections": 12,
  "accounts_with_connections": ["acc_1", "acc_2", "acc_3"]
}
```

## 🚀 CI/CD with GitHub Actions

This project includes GitHub Actions workflows for continuous integration and deployment:

### Workflows

1. **CI Workflow** (`.github/workflows/ci.yml`)
   - Runs on Python 3.13
   - Executes linting (flake8), type checking (mypy), and security scans
   - Runs all domain tests and API integration tests
   - Performs security checks with Bandit and Safety
   - Smart path detection to run tests only when relevant code changes

2. **Docker Build and Test** (`.github/workflows/docker.yml`)
   - Builds Docker images with BuildKit caching
   - Tests the containerized application with real API calls
   - Tests Docker Compose setup
   - Triggered when banking-api module changes

3. **Test Python Module** (`.github/workflows/test-python-module.yml`)
   - Reusable workflow for testing individual Python modules
   - Called by the main CI workflow for modular testing
   - Supports different Python modules independently

### Setting Up GitHub Actions

1. **Fork or clone the repository** to your GitHub account

2. **Update badge URLs** in README.md by replacing `tomaszmichalak` with your GitHub username:
   ```markdown
   [![CI](https://github.com/YOUR_USERNAME/learning-python/workflows/CI/badge.svg)]
   ```

3. **Push to main branch** to trigger workflows - the workflows use smart path detection to only run relevant tests

## �️ Data Models

### Account Model
- `account_id`: Unique identifier
- `account_holder`: Name of the account holder
- `account_type`: Type of account (checking, savings, credit)
- `balance`: Current account balance
- `created_at`: Account creation timestamp
- `is_active`: Account status

### Transaction Model
- `transaction_id`: Unique identifier
- `account_id`: Associated account
- `amount`: Transaction amount
- `transaction_type`: Type (deposit, withdrawal, transfer)
- `description`: Optional description
- `timestamp`: When the transaction occurred
- `balance_after`: Account balance after transaction

## �🚀 Architecture Overview

### Service Separation
- **REST Service** (`api/services/rest_service.py`): Handles HTTP requests and responses
- **WebSocket Service** (`api/services/websocket_service.py`): Manages real-time connections
- **WebSocket Manager** (`api/services/websocket_manager.py`): Handles connection pooling and broadcasting

### Domain-Driven Design
- **Domain Models**: Pure business entities
- **Domain Services**: Business logic implementation
- **Repositories**: Data access abstraction
- **Memory Repositories**: In-memory storage for development/testing

### Real-time Features
- **WebSocket Broadcasting**: Automatic real-time updates for transactions
- **Connection Management**: Support for global and account-specific subscriptions
- **CORS Support**: Configured for React frontend integration

## 🔌 WebSocket Implementation Details

### WebSocket Endpoints

#### Global Transaction Stream
```
ws://localhost:8000/api/ws/transactions
```
- Receives updates for all transactions across all accounts
- Ideal for admin dashboards or system monitoring

#### Account-Specific Stream
```
ws://localhost:8000/api/ws/transactions/{account_id}
```
- Receives updates only for the specified account
- Perfect for user-specific applications

#### Connection Statistics (REST)
```
GET /api/ws/stats
```
- Returns current WebSocket connection statistics
- Useful for monitoring and debugging

### Message Types

#### Incoming Messages (Client → Server)

**Ping**
```json
{
  "type": "ping"
}
```
Response: `pong` message with timestamp

**Get Statistics**
```json
{
  "type": "get_stats"
}
```
Response: Connection statistics

**Get Recent Transactions**
```json
{
  "type": "get_recent_transactions",
  "limit": 10
}
```
Response: List of recent transactions (limited by `limit` parameter)

**Get Account Balance**
```json
{
  "type": "get_account_balance"
}
```
Response: Current account balance (only for account-specific connections)

#### Outgoing Messages (Server → Client)

**Connection Established**
```json
{
  "type": "connection_established",
  "data": {
    "account_id": "account_123",
    "message": "Connected to account-specific transaction stream",
    "initial_transactions_count": 5
  }
}
```

**Transaction Update**
```json
{
  "type": "transaction_update",
  "data": {
    "transaction_id": "txn_456",
    "account_id": "account_123",
    "amount": 100.0,
    "transaction_type": "deposit",
    "description": "Salary deposit",
    "timestamp": "2025-08-21T10:30:00",
    "balance_after": 1100.0
  }
}
```

**Balance Update**
```json
{
  "type": "balance_update",
  "data": {
    "account_id": "account_123",
    "new_balance": 1100.0,
    "timestamp": 1692616200.0
  }
}
```

**Error Messages**
```json
{
  "type": "error",
  "data": {
    "message": "Account not found"
  }
}
```

### WebSocket Usage Examples

#### JavaScript Client (Browser)

```javascript
// Connect to all transactions
const ws = new WebSocket('ws://localhost:8000/api/ws/transactions');

ws.onopen = function(event) {
    console.log('Connected to WebSocket');
    
    // Send ping
    ws.send(JSON.stringify({type: 'ping'}));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'transaction_update':
            console.log('New transaction:', data.data);
            updateUI(data.data);
            break;
        case 'balance_update':
            console.log('Balance updated:', data.data);
            updateBalance(data.data);
            break;
        case 'pong':
            console.log('Pong received');
            break;
    }
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};

ws.onclose = function(event) {
    console.log('WebSocket closed:', event);
};
```

#### Python Client

```python
import asyncio
import json
import websockets

async def client():
    uri = "ws://localhost:8000/api/ws/transactions"
    
    async with websockets.connect(uri) as websocket:
        # Send ping
        await websocket.send(json.dumps({"type": "ping"}))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data['type']}")
            
            if data['type'] == 'transaction_update':
                transaction = data['data']
                print(f"New transaction: ${transaction['amount']}")

asyncio.run(client())
```

#### React Integration Example
```jsx
import { useEffect, useState } from 'react';

function TransactionStream({ accountId }) {
    const [transactions, setTransactions] = useState([]);
    const [balance, setBalance] = useState(0);
    
    useEffect(() => {
        const wsUrl = accountId 
            ? `ws://localhost:8000/api/ws/transactions/${accountId}`
            : 'ws://localhost:8000/api/ws/transactions';
            
        const ws = new WebSocket(wsUrl);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'transaction_update') {
                setTransactions(prev => [data.data, ...prev]);
            } else if (data.type === 'balance_update') {
                setBalance(data.data.new_balance);
            }
        };
        
        return () => ws.close();
    }, [accountId]);
    
    return (
        <div>
            <h3>Balance: ${balance}</h3>
            <ul>
                {transactions.map(tx => (
                    <li key={tx.transaction_id}>
                        {tx.transaction_type}: ${tx.amount}
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

### WebSocket Connection Management

#### Automatic Cleanup
- Disconnected clients are automatically removed from connection pools
- Error handling ensures robust connection management
- Memory usage is optimized by cleaning up stale connections

#### Connection Statistics
- Track total connections, global connections, and account-specific connections
- Monitor system load and performance
- Available via REST endpoint: `GET /api/ws/stats`

#### Health Monitoring
- WebSocket connections include health checks
- Ping/pong mechanism for connection validation
- Graceful handling of connection failures

### WebSocket Security Considerations

#### Authentication
- Currently, WebSocket connections are open (no authentication)
- In production, implement authentication before WebSocket upgrade
- Consider JWT tokens or session-based authentication

#### Rate Limiting
- Implement rate limiting for WebSocket messages
- Prevent spam and abuse of real-time connections
- Monitor connection patterns for anomalies

#### Data Validation
- All incoming WebSocket messages are validated
- Malformed JSON is handled gracefully
- Unknown message types return error responses

### Integration Testing
The API is designed to work with:
- **React Frontend**: Port 3000 (via NGINX proxy or direct connection)
- **WebSocket Clients**: Support for real-time transaction updates
- **Docker Compose**: Full-stack deployment

## 📋 Development Notes

- This is a demo application using in-memory storage
- In production, you would use a proper database (PostgreSQL, MySQL, etc.)
- Authentication and authorization should be implemented for production use
- Additional validations and business rules should be added
- Error handling can be enhanced further

## 🧪 Testing

### Test Organization

The project includes comprehensive tests organized by domain:

- **Domain-Specific Tests**: Each domain has its own test file
  - `domains/account/test_account.py` - Account repository and service tests
  - `domains/transaction/test_transaction.py` - Transaction repository and service tests
- **Integration Tests** (`it-tests/`): API and WebSocket integration tests
- **Comprehensive Tests** (`api/test_domains.py`): Cross-domain integration tests

### Running Tests

#### Local Test Execution

```bash
# Run all domain unit tests (RECOMMENDED)
cd api && pytest domains/ -v

# Run individual domain tests
python -m api.domains.account.test_account
python -m api.domains.transaction.test_transaction

# Run comprehensive domain tests
cd api && pytest test_domains.py -v

# Run with coverage
cd api && pytest test_domains.py --cov=domains --cov-report=html

# Run all tests
pytest -v

# Run integration tests
cd it-tests
python test_rest_api.py
pytest test_websocket.py -v
```

#### WebSocket Testing

**Using the Included Example Client**

1. Start the banking API server:
```bash
cd banking-api
python -m api.main
```

2. In another terminal, run the WebSocket client:
```bash
python tools/websocket_client_example.py
```

3. Choose option 3 to create a test account and connect
4. Use the provided cURL command to create transactions
5. Watch real-time updates in the WebSocket client

**Manual WebSocket Testing**

```bash
# Create account first
curl -X POST "http://localhost:8000/api/accounts" \
     -H "Content-Type: application/json" \
     -d '{"account_holder": "Test User", "account_type": "savings", "balance": 1000.0}'

# Create transaction (will broadcast to WebSocket clients)
curl -X POST "http://localhost:8000/api/transactions" \
     -H "Content-Type: application/json" \
     -d '{"account_id": "ACCOUNT_ID", "amount": 100.0, "transaction_type": "deposit", "description": "Test deposit"}'

# Transfer funds (will broadcast to WebSocket clients)  
curl -X POST "http://localhost:8000/api/transfers" \
     -H "Content-Type: application/json" \
     -d '{"from_account_id": "ACCOUNT_1", "to_account_id": "ACCOUNT_2", "amount": 50.0, "description": "Transfer test"}'

# Check WebSocket connection statistics
curl http://localhost:8000/api/ws/stats
```

#### Docker Test Execution

```bash
# Navigate to api directory first
cd /Users/tomaszmichalak/Projects/learning-python/banking-api/api

# Run tests in Docker container
docker compose run --rm banking-api pytest domains/ -v

# Run specific test suites
docker compose run --rm banking-api pytest test_domains.py -v
```

### Manual Testing
1. **Start the API** using one of the debug configurations
2. **Open API Documentation**: http://localhost:8000/docs
3. **Test WebSocket**: http://localhost:3000/websocket-direct-test.html
4. **Monitor logs** in VS Code Debug Console

### Integration Testing
The API is designed to work with:
- **React Frontend**: Port 3000 (via NGINX proxy or direct connection)
- **WebSocket Clients**: Support for real-time transaction updates
- **Docker Compose**: Full-stack deployment

## 🔍 Debugging Tips

### Common Issues

1. **Breakpoints not hitting in router methods**:
   - ✅ Use `USE_DEBUGGABLE_ROUTER = True`
   - ✅ Set breakpoints in `api/services/debuggable_router.py`
   - ✅ Use "Debug Banking API - No Reload" configuration

2. **WebSocket connections not working**:
   - ✅ Check CORS configuration
   - ✅ Verify WebSocket URL: `ws://localhost:8000/api/ws/transactions`
   - ✅ Monitor WebSocket manager logs
   - ✅ Test with `curl http://localhost:8000/api/ws/stats` to check connection health
   - ✅ Ensure account_id exists for account-specific connections
   - ✅ Check browser developer tools for WebSocket connection errors

3. **WebSocket messages not received**:
   - ✅ Verify WebSocket connection is established (check `connection_established` message)
   - ✅ Check if the account_id exists for account-specific streams
   - ✅ Look for error messages in the console
   - ✅ Test with ping/pong messages to verify connection health
   - ✅ Monitor connection statistics: `GET /api/ws/stats`

4. **Performance issues with WebSocket**:
   - ✅ Monitor connection statistics and memory usage
   - ✅ Check for memory leaks in connection management
   - ✅ Consider rate limiting for high-frequency updates
   - ✅ Use account-specific connections instead of global when possible

5. **Import errors**:
   - ✅ Ensure `PYTHONPATH` includes banking-api directory
   - ✅ Activate virtual environment
   - ✅ Install all requirements

### Debug Logging

Enable detailed logging by setting log level to DEBUG:
```python
logging.basicConfig(level=logging.DEBUG)
```

Look for these debug markers:
- 🐛 Router method entry/exit
- 🚀 WebSocket broadcasting
- 📨 WebSocket message content
- 🔌 WebSocket connection events
- ⚠️ Warning conditions
- 📊 Connection statistics updates

### Variable Inspection

Use VS Code's debug features:
- **Variables panel**: Inspect local and global variables
- **Debug Console**: Execute Python expressions
- **Call Stack**: Trace execution flow
- **Breakpoint conditions**: Set conditional breakpoints

## 📝 Code Style

### Naming Conventions
- **Classes**: PascalCase (e.g., `RESTService`)
- **Functions**: snake_case (e.g., `create_account`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `USE_DEBUGGABLE_ROUTER`)

### Async/Await
- All service methods are async
- Use `await` for all async calls
- Handle exceptions properly in async contexts

### Error Handling
- Use FastAPI's `HTTPException` for API errors
- Log errors with appropriate levels
- Provide meaningful error messages

## 🤝 Contributing Guidelines

1. **Before starting development**:
   - Stop Docker containers
   - Set up debugging environment
   - Enable debuggable router for development

2. **During development**:
   - Use VS Code debugger
   - Test both REST and WebSocket functionality
   - Monitor logs for errors

3. **Before committing**:
   - Test with both router implementations
   - Verify WebSocket broadcasting works
   - Check that Docker build succeeds

4. **Code review checklist**:
   - [ ] Debuggable router methods updated
   - [ ] WebSocket broadcasting tested
   - [ ] Error handling implemented
   - [ ] Logging appropriate
   - [ ] Documentation updated

##  Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **VS Code Python Debugging**: https://code.visualstudio.com/docs/python/debugging
- **WebSocket Testing**: Use browser developer tools or WebSocket testing tools
- **API Documentation**: http://localhost:8000/docs (when running)
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc

---

Happy debugging! 🐛✨
