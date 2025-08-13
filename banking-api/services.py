from typing import List, Optional
from datetime import datetime
import uuid
from models import Account, AccountCreate, Transaction, TransactionCreate, TransferRequest, TransactionType
from repositories import AccountRepository, TransactionRepository
from fastapi import HTTPException


class BankingService:
    """Service layer for banking operations."""
    
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
    
    async def create_account(self, account_create: AccountCreate) -> Account:
        """Create a new account."""
        account_id = str(uuid.uuid4())
        account = Account(
            account_id=account_id,
            account_holder=account_create.account_holder,
            account_type=account_create.account_type,
            balance=account_create.balance,
            created_at=datetime.now(),
            is_active=True
        )
        return await self.account_repository.create_account(account)
    
    async def get_account(self, account_id: str) -> Account:
        """Get an account by ID."""
        account = await self.account_repository.get_account(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
    
    async def get_all_accounts(self) -> List[Account]:
        """Get all accounts."""
        return await self.account_repository.get_all_accounts()
    
    async def update_account(self, account_id: str, account_update: AccountCreate) -> Account:
        """Update an account."""
        existing_account = await self.account_repository.get_account(account_id)
        if not existing_account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        updated_account = Account(
            account_id=account_id,
            account_holder=account_update.account_holder,
            account_type=account_update.account_type,
            balance=existing_account.balance,  # Keep existing balance
            created_at=existing_account.created_at,
            is_active=existing_account.is_active
        )
        return await self.account_repository.update_account(updated_account)
    
    async def delete_account(self, account_id: str) -> bool:
        """Delete (deactivate) an account."""
        if not await self.account_repository.account_exists(account_id):
            raise HTTPException(status_code=404, detail="Account not found")
        return await self.account_repository.delete_account(account_id)
    
    async def create_transaction(self, transaction_create: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        account = await self.account_repository.get_account(transaction_create.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        if not account.is_active:
            raise HTTPException(status_code=400, detail="Account is not active")
        
        # Calculate new balance
        if transaction_create.transaction_type == TransactionType.DEPOSIT:
            new_balance = account.balance + transaction_create.amount
        elif transaction_create.transaction_type == TransactionType.WITHDRAWAL:
            if account.balance < transaction_create.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            new_balance = account.balance - transaction_create.amount
        else:
            raise HTTPException(status_code=400, detail="Invalid transaction type for single account")
        
        # Update account balance
        account.balance = new_balance
        await self.account_repository.update_account(account)
        
        # Create transaction record
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            transaction_id=transaction_id,
            account_id=transaction_create.account_id,
            amount=transaction_create.amount,
            transaction_type=transaction_create.transaction_type,
            description=transaction_create.description,
            timestamp=datetime.now(),
            balance_after=new_balance
        )
        
        return await self.transaction_repository.create_transaction(transaction)
    
    async def transfer_funds(self, transfer_request: TransferRequest) -> List[Transaction]:
        """Transfer funds between accounts."""
        from_account = await self.account_repository.get_account(transfer_request.from_account_id)
        to_account = await self.account_repository.get_account(transfer_request.to_account_id)
        
        if not from_account:
            raise HTTPException(status_code=404, detail="Source account not found")
        if not to_account:
            raise HTTPException(status_code=404, detail="Destination account not found")
        
        if not from_account.is_active or not to_account.is_active:
            raise HTTPException(status_code=400, detail="One or both accounts are not active")
        
        if from_account.balance < transfer_request.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds in source account")
        
        # Perform the transfer
        from_account.balance -= transfer_request.amount
        to_account.balance += transfer_request.amount
        
        # Update accounts
        await self.account_repository.update_account(from_account)
        await self.account_repository.update_account(to_account)
        
        # Create transaction records
        withdrawal_id = str(uuid.uuid4())
        deposit_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        withdrawal_transaction = Transaction(
            transaction_id=withdrawal_id,
            account_id=transfer_request.from_account_id,
            amount=transfer_request.amount,
            transaction_type=TransactionType.TRANSFER,
            description=f"Transfer to {transfer_request.to_account_id}: {transfer_request.description or ''}",
            timestamp=timestamp,
            balance_after=from_account.balance
        )
        
        deposit_transaction = Transaction(
            transaction_id=deposit_id,
            account_id=transfer_request.to_account_id,
            amount=transfer_request.amount,
            transaction_type=TransactionType.TRANSFER,
            description=f"Transfer from {transfer_request.from_account_id}: {transfer_request.description or ''}",
            timestamp=timestamp,
            balance_after=to_account.balance
        )
        
        await self.transaction_repository.create_transaction(withdrawal_transaction)
        await self.transaction_repository.create_transaction(deposit_transaction)
        
        return [withdrawal_transaction, deposit_transaction]
    
    async def get_transaction(self, transaction_id: str) -> Transaction:
        """Get a transaction by ID."""
        transaction = await self.transaction_repository.get_transaction(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    async def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions."""
        transactions = await self.transaction_repository.get_all_transactions()
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        return transactions
    
    async def get_account_transactions(self, account_id: str) -> List[Transaction]:
        """Get all transactions for a specific account."""
        if not await self.account_repository.account_exists(account_id):
            raise HTTPException(status_code=404, detail="Account not found")
        
        transactions = await self.transaction_repository.get_account_transactions(account_id)
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        return transactions
