from typing import List
from datetime import datetime
import uuid
from fastapi import HTTPException
from .models import Transaction, TransactionCreate, TransferRequest, TransactionType
from .repository import TransactionRepository
from ..account.service import AccountService


class TransactionService:
    """Service layer for transaction operations."""
    
    def __init__(self, transaction_repository: TransactionRepository, account_service: AccountService):
        self.transaction_repository = transaction_repository
        self.account_service = account_service
    
    async def create_transaction(self, transaction_create: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        account = await self.account_service.get_account(transaction_create.account_id)
        
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
        await self.account_service.account_repository.update_account(account)
        
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
        from_account = await self.account_service.get_account(transfer_request.from_account_id)
        to_account = await self.account_service.get_account(transfer_request.to_account_id)
        
        if not from_account.is_active or not to_account.is_active:
            raise HTTPException(status_code=400, detail="One or both accounts are not active")
        
        if from_account.balance < transfer_request.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds in source account")
        
        # Perform the transfer
        from_account.balance -= transfer_request.amount
        to_account.balance += transfer_request.amount
        
        # Update accounts
        await self.account_service.account_repository.update_account(from_account)
        await self.account_service.account_repository.update_account(to_account)
        
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
        if not await self.account_service.account_exists(account_id):
            raise HTTPException(status_code=404, detail="Account not found")
        
        transactions = await self.transaction_repository.get_account_transactions(account_id)
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        return transactions
