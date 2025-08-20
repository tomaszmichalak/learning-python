# Banking REST API with Package-by-Feature Architecture

[![CI/CD Pipeline](https://github.com/tomaszmichalak/learning-python/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/tomaszmichalak/learning-python/actions/workflows/ci.yml)
[![Docker Build & Test](https://github.com/tomaszmichalak/learning-python/workflows/Docker%20Build%20%26%20Test/badge.svg)](https://github.com/tomaszmichalak/learning-python/actions/workflows/docker.yml)
[![Security Scan](https://github.com/tomaszmichalak/learning-python/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/tomaszmichalak/learning-python/actions/workflows/ci.yml)

This project demonstrates a clean banking REST API built with FastAPI that implements the **Package-by-Feature** approach, Repository Pattern, and follows clean architecture principles.

## Architecture Overview

The project follows a **Package-by-Feature** approach with domain-driven design:

- **Presentation Layer** (`main.py`): FastAPI endpoints that handle HTTP requests and responses
- **Domain Layer** (`domains/`): Business domains organized by feature
  - **Account Domain** (`domains/account/`): All account-related functionality
  - **Transaction Domain** (`domains/transaction/`): All transaction-related functionality

### Package-by-Feature Benefits

1. **High Cohesion**: Related functionality is grouped together
2. **Easy Navigation**: Find all account-related code in one place
3. **Domain Isolation**: Clear boundaries between business domains
4. **Scalability**: Easy to add new domains or features
5. **Team Organization**: Teams can own specific domains

## Project Structure

```
banking-api/
├── main.py                    # FastAPI application entry point
├── start_server.py           # Server startup script
├── domains/                   # Domain packages (Package-by-Feature)
│   ├── __init__.py
│   ├── account/              # Account domain
│   │   ├── __init__.py
│   │   ├── models.py         # Account models and DTOs
│   │   ├── repository.py     # Account repository interface
│   │   ├── memory_repository.py # In-memory account repository
│   │   ├── service.py        # Account business logic
│   │   └── test_account.py   # Account domain tests
│   └── transaction/          # Transaction domain
│       ├── __init__.py
│       ├── models.py         # Transaction models and DTOs
│       ├── repository.py     # Transaction repository interface
│       ├── memory_repository.py # In-memory transaction repository
│       ├── service.py        # Transaction business logic
│       └── test_transaction.py # Transaction domain tests
├── test_domains.py           # Comprehensive domain tests
├── run_domain_tests.py       # Test runner for all domains
├── test_api.py              # API integration tests
├── requirements.txt          # Project dependencies
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # This file
```

### Domain Architecture

Each domain follows a consistent structure:

- **`models.py`**: Pydantic models, domain entities, and DTOs
- **`repository.py`**: Abstract repository interface
- **`memory_repository.py`**: Concrete repository implementation
- **`service.py`**: Business logic and domain operations

## Features

- **Account Management**
  - Create new bank accounts (checking, savings, credit)
  - View account details and balance
  - Update account information
  - Deactivate accounts

- **Transaction Operations**
  - Deposit funds
  - Withdraw funds
  - Transfer funds between accounts
  - View transaction history

## Setup and Installation

### Option 1: Local Development

1. **Install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or using the start server script:
   ```bash
   python start_server.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

3. **Run tests:**
   ```bash
   # Run all domain tests (recommended)
   python run_domain_tests.py
   
   # Run individual domain tests
   python -m domains.account.test_account
   python -m domains.transaction.test_transaction
   
   # Run the comprehensive domain test suite
   pytest test_domains.py -v
   
   # Run existing API tests
   python test_api.py
   ```

### Option 2: Docker

1. **Build and run with Docker Compose:**
   ```bash
   docker compose up --build
   ```

2. **Or build and run with Docker directly:**
   ```bash
   # Build the image
   docker build -t banking-api .
   
   # Run the container
   docker run -d --name banking-api -p 8000:8000 banking-api
   ```

### Access the API
   - API: http://localhost:8000
   - Interactive API docs (Swagger): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

## Docker Commands

### Development with Docker Compose
```bash
# Start the application in development mode
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the application
docker-compose down

# View logs
docker-compose logs -f
```

### Production Docker Commands
```bash
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

## API Endpoints

### Accounts

- `POST /accounts` - Create a new account
- `GET /accounts` - Get all accounts
- `GET /accounts/{account_id}` - Get specific account
- `PUT /accounts/{account_id}` - Update account information
- `DELETE /accounts/{account_id}` - Deactivate account

### Transactions

- `POST /transactions` - Create a transaction (deposit/withdrawal)
- `POST /transfers` - Transfer funds between accounts
- `GET /transactions` - Get all transactions
- `GET /transactions/{transaction_id}` - Get specific transaction
- `GET /accounts/{account_id}/transactions` - Get account transaction history

## Example Usage

### 1. Create an Account

```bash
curl -X POST "http://localhost:8000/accounts" \
     -H "Content-Type: application/json" \
     -d '{
       "account_holder": "John Doe",
       "account_type": "checking",
       "balance": 1000.00
     }'
```

### 2. Make a Deposit

```bash
curl -X POST "http://localhost:8000/transactions" \
     -H "Content-Type: application/json" \
     -d '{
       "account_id": "your-account-id",
       "amount": 500.00,
       "transaction_type": "deposit",
       "description": "Salary deposit"
     }'
```

### 3. Make a Withdrawal

```bash
curl -X POST "http://localhost:8000/transactions" \
     -H "Content-Type: application/json" \
     -d '{
       "account_id": "your-account-id",
       "amount": 200.00,
       "transaction_type": "withdrawal",
       "description": "ATM withdrawal"
     }'
```

### 4. Transfer Funds

```bash
curl -X POST "http://localhost:8000/transfers" \
     -H "Content-Type: application/json" \
     -d '{
       "from_account_id": "source-account-id",
       "to_account_id": "destination-account-id",
       "amount": 300.00,
       "description": "Payment to friend"
     }'
```

## Data Models

### Account
- `account_id`: Unique identifier
- `account_holder`: Name of the account holder
- `account_type`: Type of account (checking, savings, credit)
- `balance`: Current account balance
- `created_at`: Account creation timestamp
- `is_active`: Account status

### Transaction
- `transaction_id`: Unique identifier
- `account_id`: Associated account
- `amount`: Transaction amount
- `transaction_type`: Type (deposit, withdrawal, transfer)
- `description`: Optional description
- `timestamp`: When the transaction occurred
- `balance_after`: Account balance after transaction

## Notes

- This is a demo application using in-memory storage
- In production, you would use a proper database (PostgreSQL, MySQL, etc.)
- Authentication and authorization should be implemented for production use
- Additional validations and business rules should be added
- Error handling can be enhanced further

## Testing

The project includes comprehensive tests organized by domain:

- **Domain-Specific Tests**: Each domain has its own test file
  - `domains/account/test_account.py` - Account repository and service tests
  - `domains/transaction/test_transaction.py` - Transaction repository and service tests
- **Test Runner** (`run_domain_tests.py`): Runs all domain tests with clear reporting
- **Comprehensive Tests** (`test_domains.py`): Cross-domain integration tests

```bash
# Run all domain tests with clear reporting
python run_domain_tests.py

# Run individual domain tests
python -m domains.account.test_account
python -m domains.transaction.test_transaction

# Run comprehensive domain tests
pytest test_domains.py -v

# Run with coverage
pytest test_domains.py --cov=domains --cov-report=html

# Run all tests
pytest -v

# Run existing API integration tests
python test_api.py
```

## CI/CD with GitHub Actions

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

2. **Update badge URLs** in README.md by replacing `tomaszmichalak` with your GitHub tomaszmichalak:
   ```markdown
   [![CI](https://github.com/YOUR_tomaszmichalak/learning-python/workflows/CI/badge.svg)]
   ```

3. **Push to main branch** to trigger workflows - the workflows use smart path detection to only run relevant tests

#```

## Security Configuration

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
python start_server.py
# Starts on 127.0.0.1:8000

# Allow external connections (if needed for development)
HOST=0.0.0.0 python start_server.py
# Starts on 0.0.0.0:8000

# Custom port
PORT=3000 python start_server.py
# Starts on 127.0.0.1:3000
```

#### Docker Environments

In Docker containers, `0.0.0.0` binding is automatically used and is safe within the container environment:

```dockerfile
# Dockerfile uses 0.0.0.0 binding (safe in containers)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  # nosec B104
```

The `# nosec B104` comment tells security scanners that this usage is intentional and reviewed.

### Security Notes

- Never bind to `0.0.0.0` on production servers unless behind proper firewall/proxy
- Use environment variables for configuration instead of hardcoded values
- Container binding to `0.0.0.0` is safe within container networking
- - Always review security scan findings and apply appropriate mitigations

````
