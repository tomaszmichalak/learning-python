from fastapi import FastAPI, HTTPException
from typing import List, Dict
from datetime import datetime
import uuid
from models import (
    Account, AccountCreate, Transaction, TransactionCreate, 
    TransferRequest, TransactionType
)

app = FastAPI(
    title="Banking API",
    description="A simple banking REST API with accounts and transactions",
    version="1.0.0"
)

# In-memory storage (in production, you'd use a database)
accounts: Dict[str, Account] = {}
transactions: Dict[str, Transaction] = {}


@app.get("/")
async def root():
    """Welcome endpoint"""
    return {"message": "Welcome to Banking API"}


@app.post("/accounts", response_model=Account)
async def create_account(account: AccountCreate):
    """Create a new bank account"""
    account_id = str(uuid.uuid4())
    new_account = Account(
        account_id=account_id,
        account_holder=account.account_holder,
        account_type=account.account_type,
        balance=account.balance,
        created_at=datetime.now(),
        is_active=True
    )
    accounts[account_id] = new_account
    return new_account


@app.get("/accounts", response_model=List[Account])
async def get_all_accounts():
    """Get all accounts"""
    return list(accounts.values())


@app.get("/accounts/{account_id}", response_model=Account)
async def get_account(account_id: str):
    """Get a specific account by ID"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id]


@app.put("/accounts/{account_id}", response_model=Account)
async def update_account(account_id: str, account_update: AccountCreate):
    """Update an existing account"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    existing_account = accounts[account_id]
    updated_account = Account(
        account_id=account_id,
        account_holder=account_update.account_holder,
        account_type=account_update.account_type,
        balance=existing_account.balance,  # Keep existing balance
        created_at=existing_account.created_at,
        is_active=existing_account.is_active
    )
    accounts[account_id] = updated_account
    return updated_account


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: str):
    """Deactivate an account (soft delete)"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    accounts[account_id].is_active = False
    return {"message": f"Account {account_id} has been deactivated"}


@app.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction"""
    if transaction.account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account = accounts[transaction.account_id]
    if not account.is_active:
        raise HTTPException(status_code=400, detail="Account is not active")
    
    # Calculate new balance
    if transaction.transaction_type == TransactionType.DEPOSIT:
        new_balance = account.balance + transaction.amount
    elif transaction.transaction_type == TransactionType.WITHDRAWAL:
        if account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        new_balance = account.balance - transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type for single account")
    
    # Update account balance
    account.balance = new_balance
    
    # Create transaction record
    transaction_id = str(uuid.uuid4())
    new_transaction = Transaction(
        transaction_id=transaction_id,
        account_id=transaction.account_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        description=transaction.description,
        timestamp=datetime.now(),
        balance_after=new_balance
    )
    
    transactions[transaction_id] = new_transaction
    return new_transaction


@app.post("/transfers", response_model=List[Transaction])
async def transfer_funds(transfer: TransferRequest):
    """Transfer funds between accounts"""
    if transfer.from_account_id not in accounts:
        raise HTTPException(status_code=404, detail="Source account not found")
    if transfer.to_account_id not in accounts:
        raise HTTPException(status_code=404, detail="Destination account not found")
    
    from_account = accounts[transfer.from_account_id]
    to_account = accounts[transfer.to_account_id]
    
    if not from_account.is_active or not to_account.is_active:
        raise HTTPException(status_code=400, detail="One or both accounts are not active")
    
    if from_account.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in source account")
    
    # Perform the transfer
    from_account.balance -= transfer.amount
    to_account.balance += transfer.amount
    
    # Create transaction records
    withdrawal_id = str(uuid.uuid4())
    deposit_id = str(uuid.uuid4())
    
    withdrawal_transaction = Transaction(
        transaction_id=withdrawal_id,
        account_id=transfer.from_account_id,
        amount=transfer.amount,
        transaction_type=TransactionType.TRANSFER,
        description=f"Transfer to {transfer.to_account_id}: {transfer.description or ''}",
        timestamp=datetime.now(),
        balance_after=from_account.balance
    )
    
    deposit_transaction = Transaction(
        transaction_id=deposit_id,
        account_id=transfer.to_account_id,
        amount=transfer.amount,
        transaction_type=TransactionType.TRANSFER,
        description=f"Transfer from {transfer.from_account_id}: {transfer.description or ''}",
        timestamp=datetime.now(),
        balance_after=to_account.balance
    )
    
    transactions[withdrawal_id] = withdrawal_transaction
    transactions[deposit_id] = deposit_transaction
    
    return [withdrawal_transaction, deposit_transaction]


@app.get("/accounts/{account_id}/transactions", response_model=List[Transaction])
async def get_account_transactions(account_id: str):
    """Get all transactions for a specific account"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_transactions = [
        transaction for transaction in transactions.values()
        if transaction.account_id == account_id
    ]
    
    # Sort by timestamp (newest first)
    account_transactions.sort(key=lambda x: x.timestamp, reverse=True)
    return account_transactions


@app.get("/transactions", response_model=List[Transaction])
async def get_all_transactions():
    """Get all transactions"""
    all_transactions = list(transactions.values())
    all_transactions.sort(key=lambda x: x.timestamp, reverse=True)
    return all_transactions


@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str):
    """Get a specific transaction by ID"""
    if transaction_id not in transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transactions[transaction_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
