# Banking REST API

[![CI/CD Pipeline](https://github.com/tomaszmichalak/learning-python/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/tomaszmichalak/learning-python/actions/workflows/ci.yml)
[![Docker Build & Test](https://github.com/tomaszmichalak/learning-python/workflows/Docker%20Build%20%26%20Test/badge.svg)](https://github.com/tomaszmichalak/learning-python/actions/workflows/docker.yml)

A modern banking REST API built with FastAPI that provides account management and transaction processing with real-time WebSocket updates.

## 🚀 Quick Start

### Run with Docker (Recommended)

```bash
cd api
docker compose up --build
```

### Run Locally

```bash
# Install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r api/requirements.txt

# Start the server
python api/start_server.py
```

### Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## 📋 Available APIs

### Account Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts` | Create a new bank account |
| GET | `/accounts` | List all accounts |
| GET | `/accounts/{account_id}` | Get account details |
| PUT | `/accounts/{account_id}` | Update account information |
| DELETE | `/accounts/{account_id}` | Deactivate account |

### Transaction Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions` | Create transaction (deposit/withdrawal) |
| POST | `/transfers` | Transfer funds between accounts |
| GET | `/transactions` | List all transactions |
| GET | `/transactions/{transaction_id}` | Get transaction details |
| GET | `/accounts/{account_id}/transactions` | Get account transaction history |

### Real-time Updates (WebSocket)

| Endpoint | Description |
|----------|-------------|
| `/ws/transactions` | Real-time updates for all transactions |
| `/ws/transactions/{account_id}` | Real-time updates for specific account |

## 💡 Basic Usage Flow

### Step 1: Create Two Accounts

```bash
# Create first account (John's checking account)
curl -X POST "http://localhost:8000/accounts" \
     -H "Content-Type: application/json" \
     -d '{
       "account_holder": "John Doe",
       "account_type": "checking",
       "balance": 1000.00
     }'
```

**Response:**
```json
{
  "account_id": "acc_001",
  "account_holder": "John Doe",
  "account_type": "checking",
  "balance": 1000.00,
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

```bash
# Create second account (Jane's savings account)
curl -X POST "http://localhost:8000/accounts" \
     -H "Content-Type: application/json" \
     -d '{
       "account_holder": "Jane Smith",
       "account_type": "savings",
       "balance": 500.00
     }'
```

**Response:**
```json
{
  "account_id": "acc_002",
  "account_holder": "Jane Smith",
  "account_type": "savings",
  "balance": 500.00,
  "created_at": "2024-01-15T10:31:00Z",
  "is_active": true
}
```

### Step 2: Make a Deposit

```bash
# Deposit $200 to John's account
curl -X POST "http://localhost:8000/transactions" \
     -H "Content-Type: application/json" \
     -d '{
       "account_id": "acc_001",
       "amount": 200.00,
       "transaction_type": "deposit",
       "description": "Salary deposit"
     }'
```

**Response:**
```json
{
  "transaction_id": "txn_001",
  "account_id": "acc_001",
  "amount": 200.00,
  "transaction_type": "deposit",
  "description": "Salary deposit",
  "timestamp": "2024-01-15T10:32:00Z",
  "balance_after": 1200.00
}
```

### Step 3: Transfer Money Between Accounts

```bash
# Transfer $300 from John to Jane
curl -X POST "http://localhost:8000/transfers" \
     -H "Content-Type: application/json" \
     -d '{
       "from_account_id": "acc_001",
       "to_account_id": "acc_002",
       "amount": 300.00,
       "description": "Payment to Jane"
     }'
```

**Response:**
```json
[
  {
    "transaction_id": "txn_002",
    "account_id": "acc_001",
    "amount": -300.00,
    "transaction_type": "transfer",
    "description": "Transfer to acc_002: Payment to Jane",
    "timestamp": "2024-01-15T10:33:00Z",
    "balance_after": 900.00
  },
  {
    "transaction_id": "txn_003",
    "account_id": "acc_002",
    "amount": 300.00,
    "transaction_type": "transfer",
    "description": "Transfer from acc_001: Payment to Jane",
    "timestamp": "2024-01-15T10:33:00Z",
    "balance_after": 800.00
  }
]
```

### Step 4: Check Account Balance

```bash
# Check John's account after the transfer
curl -X GET "http://localhost:8000/accounts/acc_001"
```

**Response:**
```json
{
  "account_id": "acc_001",
  "account_holder": "John Doe",
  "account_type": "checking",
  "balance": 900.00,
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

### Step 5: View Transaction History

```bash
# Get John's transaction history
curl -X GET "http://localhost:8000/accounts/acc_001/transactions"
```

**Response:**
```json
[
  {
    "transaction_id": "txn_002",
    "account_id": "acc_001",
    "amount": -300.00,
    "transaction_type": "transfer",
    "description": "Transfer to acc_002: Payment to Jane",
    "timestamp": "2024-01-15T10:33:00Z",
    "balance_after": 900.00
  },
  {
    "transaction_id": "txn_001",
    "account_id": "acc_001",
    "amount": 200.00,
    "transaction_type": "deposit",
    "description": "Salary deposit",
    "timestamp": "2024-01-15T10:32:00Z",
    "balance_after": 1200.00
  }
]
```

## 🔄 Real-time Updates

The API supports WebSocket connections for real-time transaction updates:

```javascript
// Connect to WebSocket for all transactions
const ws = new WebSocket('ws://localhost:8000/ws/transactions');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('New transaction:', data);
};

// Connect to WebSocket for specific account
const accountWs = new WebSocket('ws://localhost:8000/ws/transactions/acc_001');
```

## 📊 Data Models

### Account Model
```json
{
  "account_id": "string",
  "account_holder": "string",
  "account_type": "checking | savings | credit",
  "balance": 0.0,
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

### Transaction Model
```json
{
  "transaction_id": "string",
  "account_id": "string",
  "amount": 0.0,
  "transaction_type": "deposit | withdrawal | transfer",
  "description": "string",
  "timestamp": "2024-01-15T10:30:00Z",
  "balance_after": 0.0
}
```

## 🐳 Docker Commands

```bash
# Navigate to api directory first
cd api

# Run the application
docker compose up --build

# Run in background
docker compose up -d --build

# View logs
docker compose logs -f

# Stop the application
docker compose down

# Build production image
docker build -t banking-api:latest .
```

## 🔧 Environment Configuration

```bash
# Host binding (default: 127.0.0.1 for local development)
export HOST=127.0.0.1

# Port (default: 8000)
export PORT=8000

# Example: Run on different port
PORT=3000 python api/start_server.py
```

## 📝 Notes

- This is a demo application using in-memory storage
- All data is reset when the server restarts
- Account IDs and transaction IDs are auto-generated
- WebSocket connections provide real-time transaction updates
- For production use, implement proper database storage and authentication

## 🛠️ Development

For detailed development setup, testing instructions, and contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📜 License

This project is for educational purposes and demonstration of FastAPI capabilities.
