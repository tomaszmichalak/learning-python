from fastapi import FastAPI
from typing import List

# Import from domain packages
from domains.account.models import Account, AccountCreate
from domains.account.memory_repository import InMemoryAccountRepository
from domains.account.service import AccountService

from domains.transaction.models import Transaction, TransactionCreate, TransferRequest
from domains.transaction.memory_repository import InMemoryTransactionRepository
from domains.transaction.service import TransactionService

app = FastAPI(
    title="Banking API",
    description="A simple banking REST API with accounts and transactions - Package by Feature",
    version="2.0.0"
)

# Initialize repositories and services
account_repository = InMemoryAccountRepository()
transaction_repository = InMemoryTransactionRepository()

account_service = AccountService(account_repository)
transaction_service = TransactionService(transaction_repository, account_service)


@app.get("/")
async def root():
    """Welcome endpoint"""
    return {"message": "Welcome to Banking API"}


@app.post("/accounts", response_model=Account)
async def create_account(account: AccountCreate):
    """Create a new bank account"""
    return await account_service.create_account(account)


@app.get("/accounts", response_model=List[Account])
async def get_all_accounts():
    """Get all accounts"""
    return await account_service.get_all_accounts()


@app.get("/accounts/{account_id}", response_model=Account)
async def get_account(account_id: str):
    """Get a specific account by ID"""
    return await account_service.get_account(account_id)


@app.put("/accounts/{account_id}", response_model=Account)
async def update_account(account_id: str, account_update: AccountCreate):
    """Update an existing account"""
    return await account_service.update_account(account_id, account_update)


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: str):
    """Deactivate an account (soft delete)"""
    await account_service.delete_account(account_id)
    return {"message": f"Account {account_id} has been deactivated"}


@app.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction"""
    return await transaction_service.create_transaction(transaction)


@app.post("/transfers", response_model=List[Transaction])
async def transfer_funds(transfer: TransferRequest):
    """Transfer funds between accounts"""
    return await transaction_service.transfer_funds(transfer)


@app.get("/accounts/{account_id}/transactions", response_model=List[Transaction])
async def get_account_transactions(account_id: str):
    """Get all transactions for a specific account"""
    return await transaction_service.get_account_transactions(account_id)


@app.get("/transactions", response_model=List[Transaction])
async def get_all_transactions():
    """Get all transactions"""
    return await transaction_service.get_all_transactions()


@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str):
    """Get a specific transaction by ID"""
    return await transaction_service.get_transaction(transaction_id)

# simple change to validate CI
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use localhost for local development, 0.0.0.0 only when explicitly configured
    # This prevents the security scanner from flagging hardcoded bind-all-interfaces
    host = os.getenv("HOST", "127.0.0.1")  # Default to localhost for security
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)
