# Banking REST API with FastAPI

This project is generated with Claude AI and is a simple banking REST API built with FastAPI that demonstrates account management and transaction operations.

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
