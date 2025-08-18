from typing import List, Optional, Dict
from .repository import TransactionRepository
from .models import Transaction


class InMemoryTransactionRepository(TransactionRepository):
    """In-memory implementation of TransactionRepository."""
    
    def __init__(self):
        self._transactions: Dict[str, Transaction] = {}
    
    async def create_transaction(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        self._transactions[transaction.transaction_id] = transaction
        return transaction
    
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a transaction by ID."""
        return self._transactions.get(transaction_id)
    
    async def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions."""
        return list(self._transactions.values())
    
    async def get_account_transactions(self, account_id: str) -> List[Transaction]:
        """Get all transactions for a specific account."""
        return [t for t in self._transactions.values() if t.account_id == account_id]
