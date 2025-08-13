# Banking REST API with Repository Pattern

This project demonstrates a clean banking REST API built with FastAPI that implements the Repository Pattern and follows clean architecture principles.

## Architecture Overview

The project follows a layered architecture:

- **Presentation Layer** (`main.py`): FastAPI endpoints that handle HTTP requests and responses
- **Service Layer** (`services.py`): Business logic and orchestration of operations
- **Repository Layer** (`repositories.py`, `memory_repository.py`): Data access abstraction
- **Domain Layer** (`models.py`): Data models and domain entities

### Repository Pattern Benefits

1. **Separation of Concerns**: Business logic is separated from data access logic
2. **Testability**: Easy to mock repositories for unit testing
3. **Flexibility**: Can easily swap data storage implementations (memory, database, etc.)
4. **SOLID Principles**: Follows Dependency Inversion and Single Responsibility principles

## Project Structure

```
banking-api/
├── main.py                 # FastAPI application and route handlers
├── models.py              # Pydantic models and domain entities
├── repositories.py        # Abstract repository interfaces
├── memory_repository.py   # In-memory repository implementations
├── services.py           # Business logic layer
├── test_repositories.py  # Unit tests for the repository pattern
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

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
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

3. **Run tests:**
   ```bash
   # Run the repository pattern tests
   pytest test_repositories.py -v
   
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

The project includes comprehensive tests for the repository pattern:

- **Repository Tests**: Test the abstract repository interfaces and implementations
- **Service Layer Tests**: Test business logic in isolation
- **Integration Tests**: Test the full flow from API to data storage

```bash
# Run all repository pattern tests
pytest test_repositories.py -v

# Run with coverage
pytest test_repositories.py --cov=. --cov-report=html

# Run existing API integration tests
python test_api.py
```
