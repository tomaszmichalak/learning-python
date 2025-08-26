"""Alternative router structure for better debugging."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from domains.account.models import Account, AccountCreate
from domains.transaction.models import Transaction, TransactionCreate, TransferRequest


class BankingAPIRouter:
    """Banking API router class with methods that can be easily debugged."""
    
    def __init__(self, rest_service):
        self.rest_service = rest_service
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all API routes."""
        # Account routes
        self.router.add_api_route("/accounts", self.create_account, methods=["POST"], response_model=Account)
        self.router.add_api_route("/accounts", self.get_all_accounts, methods=["GET"], response_model=List[Account])
        self.router.add_api_route("/accounts/{account_id}", self.get_account, methods=["GET"], response_model=Account)
        self.router.add_api_route("/accounts/{account_id}", self.update_account, methods=["PUT"], response_model=Account)
        self.router.add_api_route("/accounts/{account_id}", self.delete_account, methods=["DELETE"])
        
        # Transaction routes
        self.router.add_api_route("/transactions", self.create_transaction, methods=["POST"], response_model=Transaction)
        self.router.add_api_route("/transactions", self.get_all_transactions, methods=["GET"], response_model=List[Transaction])
        self.router.add_api_route("/transactions/{transaction_id}", self.get_transaction, methods=["GET"], response_model=Transaction)
        self.router.add_api_route("/accounts/{account_id}/transactions", self.get_account_transactions, methods=["GET"], response_model=List[Transaction])
        
        # Transfer routes
        self.router.add_api_route("/transfers", self.transfer_funds, methods=["POST"], response_model=List[Transaction])
    
    # Account methods
    async def create_account(self, account: AccountCreate):
        """Create a new bank account - easier to debug than nested functions."""
        return await self.rest_service.create_account(account)
    
    async def get_all_accounts(self):
        """Get all accounts - easier to debug than nested functions."""
        return await self.rest_service.get_all_accounts()
    
    async def get_account(self, account_id: str):
        """Get a specific account by ID - easier to debug than nested functions."""
        return await self.rest_service.get_account(account_id)
    
    async def update_account(self, account_id: str, account_update: AccountCreate):
        """Update an existing account - easier to debug than nested functions."""
        return await self.rest_service.update_account(account_id, account_update)
    
    async def delete_account(self, account_id: str):
        """Deactivate an account (soft delete) - easier to debug than nested functions."""
        return await self.rest_service.delete_account(account_id)
    
    # Transaction methods
    async def create_transaction(self, transaction: TransactionCreate):
        """Create a new transaction - easier to debug than nested functions."""
        return await self.rest_service.create_transaction(transaction)
    
    async def get_all_transactions(self):
        """Get all transactions - easier to debug than nested functions."""
        return await self.rest_service.get_all_transactions()
    
    async def get_transaction(self, transaction_id: str):
        """Get a specific transaction by ID - easier to debug than nested functions."""
        return await self.rest_service.get_transaction(transaction_id)
    
    async def get_account_transactions(self, account_id: str):
        """Get all transactions for a specific account - easier to debug than nested functions."""
        return await self.rest_service.get_account_transactions(account_id)
    
    # Transfer methods
    async def transfer_funds(self, transfer: TransferRequest):
        """Transfer funds between accounts - easier to debug than nested functions."""
        return await self.rest_service.transfer_funds(transfer)


def create_debuggable_router(rest_service) -> APIRouter:
    """Create a debuggable router instance."""
    banking_router = BankingAPIRouter(rest_service)
    return banking_router.router


# Alternative debugging function for even easier debugging
def create_simple_debuggable_router(rest_service) -> APIRouter:
    """Create a simple debuggable router with individual functions."""
    router = APIRouter()
    
    @router.post("/accounts", response_model=Account)
    async def create_account_endpoint(account: AccountCreate):
        # This is a standalone function that's easier to set breakpoints on
        result = await rest_service.create_account(account)
        return result
    
    @router.get("/accounts", response_model=List[Account])
    async def get_all_accounts_endpoint():
        # This is a standalone function that's easier to set breakpoints on
        result = await rest_service.get_all_accounts()
        return result
    
    @router.get("/accounts/{account_id}", response_model=Account)
    async def get_account_endpoint(account_id: str):
        # This is a standalone function that's easier to set breakpoints on
        result = await rest_service.get_account(account_id)
        return result
    
    @router.put("/accounts/{account_id}", response_model=Account)
    async def update_account_endpoint(account_id: str, account_update: AccountCreate):
        # This is a standalone function that's easier to set breakpoints on
        result = await rest_service.update_account(account_id, account_update)
        return result
    
    @router.delete("/accounts/{account_id}")
    async def delete_account_endpoint(account_id: str):
        # This is a standalone function that's easier to set breakpoints on
        result = await rest_service.delete_account(account_id)
        return result
    
    return router
