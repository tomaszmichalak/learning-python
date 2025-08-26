from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Transaction


class TransactionRepository(ABC):
    """Abstract base class for transaction repository implementations."""
    
    @abstractmethod
    async def create_transaction(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        pass
    
    @abstractmethod
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a transaction by ID."""
        pass
    
    @abstractmethod
    async def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions."""
        pass
    
    @abstractmethod
    async def get_account_transactions(self, account_id: str) -> List[Transaction]:
        """Get all transactions for a specific account."""
        pass
