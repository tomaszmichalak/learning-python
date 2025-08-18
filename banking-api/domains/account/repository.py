from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Account


class AccountRepository(ABC):
    """Abstract base class for account repository implementations."""
    
    @abstractmethod
    async def create_account(self, account: Account) -> Account:
        """Create a new account."""
        pass
    
    @abstractmethod
    async def get_account(self, account_id: str) -> Optional[Account]:
        """Get an account by ID."""
        pass
    
    @abstractmethod
    async def get_all_accounts(self) -> List[Account]:
        """Get all accounts."""
        pass
    
    @abstractmethod
    async def update_account(self, account: Account) -> Account:
        """Update an existing account."""
        pass
    
    @abstractmethod
    async def delete_account(self, account_id: str) -> bool:
        """Deactivate an account (soft delete)."""
        pass
    
    @abstractmethod
    async def account_exists(self, account_id: str) -> bool:
        """Check if an account exists."""
        pass
