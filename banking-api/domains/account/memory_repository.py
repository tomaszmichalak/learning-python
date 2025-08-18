from typing import List, Optional, Dict
from .repository import AccountRepository
from .models import Account


class InMemoryAccountRepository(AccountRepository):
    """In-memory implementation of AccountRepository."""
    
    def __init__(self):
        self._accounts: Dict[str, Account] = {}
    
    async def create_account(self, account: Account) -> Account:
        """Create a new account."""
        self._accounts[account.account_id] = account
        return account
    
    async def get_account(self, account_id: str) -> Optional[Account]:
        """Get an account by ID."""
        return self._accounts.get(account_id)
    
    async def get_all_accounts(self) -> List[Account]:
        """Get all accounts."""
        return [acc for acc in self._accounts.values() if acc.is_active]
    
    async def update_account(self, account: Account) -> Account:
        """Update an existing account."""
        if account.account_id not in self._accounts:
            raise ValueError(f"Account {account.account_id} not found")
        self._accounts[account.account_id] = account
        return account
    
    async def delete_account(self, account_id: str) -> bool:
        """Deactivate an account (soft delete)."""
        account = self._accounts.get(account_id)
        if account:
            account.is_active = False
            return True
        return False
    
    async def account_exists(self, account_id: str) -> bool:
        """Check if an account exists and is active."""
        account = self._accounts.get(account_id)
        return account is not None and account.is_active
