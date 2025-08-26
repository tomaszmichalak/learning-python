from typing import List
from datetime import datetime
import uuid
from fastapi import HTTPException
from .models import Account, AccountCreate
from .repository import AccountRepository


class AccountService:
    """Service layer for account operations."""
    
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository
    
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
    
    async def account_exists(self, account_id: str) -> bool:
        """Check if an account exists."""
        return await self.account_repository.account_exists(account_id)
