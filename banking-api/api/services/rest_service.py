"""REST API routes for banking operations."""

from fastapi import APIRouter, HTTPException
from typing import List

# Import from domain packages
from domains.account.models import Account, AccountCreate
from domains.transaction.models import Transaction, TransactionCreate, TransferRequest


class RESTService:
    """REST API service for banking operations."""
    
    def __init__(self, account_service, transaction_service, websocket_manager):
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.websocket_manager = websocket_manager
    
    # Account endpoints
    async def create_account(self, account: AccountCreate) -> Account:
        """Create a new bank account."""
        return await self.account_service.create_account(account)
    
    async def get_all_accounts(self) -> List[Account]:
        """Get all accounts."""
        return await self.account_service.get_all_accounts()
    
    async def get_account(self, account_id: str) -> Account:
        """Get a specific account by ID."""
        return await self.account_service.get_account(account_id)
    
    async def update_account(self, account_id: str, account_update: AccountCreate) -> Account:
        """Update an existing account."""
        return await self.account_service.update_account(account_id, account_update)
    
    async def delete_account(self, account_id: str):
        """Deactivate an account (soft delete)."""
        await self.account_service.delete_account(account_id)
        return {"message": f"Account {account_id} has been deactivated"}
    
    # Transaction endpoints
    async def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        """Create a new transaction and broadcast to WebSocket clients."""
        # Create the transaction
        new_transaction = await self.transaction_service.create_transaction(transaction)
        
        # Broadcast to WebSocket clients
        await self.websocket_manager.broadcast_transaction(new_transaction)
        
        # Get updated account balance and broadcast
        account = await self.account_service.get_account(transaction.account_id)
        await self.websocket_manager.broadcast_account_balance(
            account.account_id, 
            account.balance
        )
        
        return new_transaction
    
    async def transfer_funds(self, transfer: TransferRequest) -> List[Transaction]:
        """Transfer funds between accounts and broadcast to WebSocket clients."""
        # Perform the transfer
        transactions = await self.transaction_service.transfer_funds(transfer)
        
        # Broadcast each transaction to WebSocket clients
        for transaction in transactions:
            await self.websocket_manager.broadcast_transaction(transaction)
        
        # Broadcast updated balances for both accounts
        from_account = await self.account_service.get_account(transfer.from_account_id)
        to_account = await self.account_service.get_account(transfer.to_account_id)
        
        await self.websocket_manager.broadcast_account_balance(
            from_account.account_id, 
            from_account.balance
        )
        await self.websocket_manager.broadcast_account_balance(
            to_account.account_id, 
            to_account.balance
        )
        
        return transactions
    
    async def get_account_transactions(self, account_id: str) -> List[Transaction]:
        """Get all transactions for a specific account."""
        return await self.transaction_service.get_account_transactions(account_id)
    
    async def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions."""
        return await self.transaction_service.get_all_transactions()
    
    async def get_transaction(self, transaction_id: str) -> Transaction:
        """Get a specific transaction by ID."""
        return await self.transaction_service.get_transaction(transaction_id)


def create_rest_router(rest_service: RESTService) -> APIRouter:
    """Create and configure the REST API router."""
    
    router = APIRouter()
    
    @router.post("/accounts", response_model=Account)
    async def create_account(account: AccountCreate):
        """Create a new bank account"""
        return await rest_service.create_account(account)
    
    @router.get("/accounts", response_model=List[Account])
    async def get_all_accounts():
        """Get all accounts"""
        return await rest_service.get_all_accounts()
    
    @router.get("/accounts/{account_id}", response_model=Account)
    async def get_account(account_id: str):
        """Get a specific account by ID"""
        return await rest_service.get_account(account_id)
    
    @router.put("/accounts/{account_id}", response_model=Account)
    async def update_account(account_id: str, account_update: AccountCreate):
        """Update an existing account"""
        return await rest_service.update_account(account_id, account_update)
    
    @router.delete("/accounts/{account_id}")
    async def delete_account(account_id: str):
        """Deactivate an account (soft delete)"""
        return await rest_service.delete_account(account_id)
    
    @router.post("/transactions", response_model=Transaction)
    async def create_transaction(transaction: TransactionCreate):
        """Create a new transaction"""
        return await rest_service.create_transaction(transaction)
    
    @router.post("/transfers", response_model=List[Transaction])
    async def transfer_funds(transfer: TransferRequest):
        """Transfer funds between accounts"""
        return await rest_service.transfer_funds(transfer)
    
    @router.get("/accounts/{account_id}/transactions", response_model=List[Transaction])
    async def get_account_transactions(account_id: str):
        """Get all transactions for a specific account"""
        return await rest_service.get_account_transactions(account_id)
    
    @router.get("/transactions", response_model=List[Transaction])
    async def get_all_transactions():
        """Get all transactions"""
        return await rest_service.get_all_transactions()
    
    @router.get("/transactions/{transaction_id}", response_model=Transaction)
    async def get_transaction(transaction_id: str):
        """Get a specific transaction by ID"""
        return await rest_service.get_transaction(transaction_id)
    
    return router
