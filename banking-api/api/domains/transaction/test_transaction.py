import pytest
import asyncio
from datetime import datetime
from .models import Transaction, TransactionCreate, TransferRequest, TransactionType
from .memory_repository import InMemoryTransactionRepository
from .service import TransactionService

# Import from account domain for dependencies
from ..account.models import Account, AccountCreate, AccountType
from ..account.memory_repository import InMemoryAccountRepository
from ..account.service import AccountService


@pytest.mark.asyncio
async def test_transaction_repository():
    """Test transaction repository operations."""
    repo = InMemoryTransactionRepository()
    
    # Create transaction
    transaction = Transaction(
        transaction_id="txn-123",
        account_id="acc-123",
        amount=100.0,
        transaction_type=TransactionType.DEPOSIT,
        description="Test deposit",
        timestamp=datetime.now(),
        balance_after=1100.0
    )
    
    created_transaction = await repo.create_transaction(transaction)
    assert created_transaction.transaction_id == "txn-123"
    assert created_transaction.amount == 100.0
    
    # Get transaction
    retrieved_transaction = await repo.get_transaction("txn-123")
    assert retrieved_transaction is not None
    assert retrieved_transaction.description == "Test deposit"
    
    # Get all transactions
    all_transactions = await repo.get_all_transactions()
    assert len(all_transactions) == 1
    
    # Get account transactions
    account_transactions = await repo.get_account_transactions("acc-123")
    assert len(account_transactions) == 1
    assert account_transactions[0].account_id == "acc-123"


@pytest.mark.asyncio
async def test_transaction_service():
    """Test transaction service operations."""
    # Setup dependencies
    account_repo = InMemoryAccountRepository()
    account_service = AccountService(account_repo)
    transaction_repo = InMemoryTransactionRepository()
    transaction_service = TransactionService(transaction_repo, account_service)
    
    # Create account first
    account_create = AccountCreate(
        account_holder="Bob Wilson",
        account_type=AccountType.CHECKING,
        balance=500.0
    )
    account = await account_service.create_account(account_create)
    
    # Create deposit transaction
    deposit = TransactionCreate(
        account_id=account.account_id,
        amount=200.0,
        transaction_type=TransactionType.DEPOSIT,
        description="Test deposit"
    )
    
    deposit_transaction = await transaction_service.create_transaction(deposit)
    assert deposit_transaction.amount == 200.0
    assert deposit_transaction.transaction_type == TransactionType.DEPOSIT
    
    # Check account balance updated
    updated_account = await account_service.get_account(account.account_id)
    assert updated_account.balance == 700.0
    
    # Create withdrawal transaction
    withdrawal = TransactionCreate(
        account_id=account.account_id,
        amount=150.0,
        transaction_type=TransactionType.WITHDRAWAL,
        description="Test withdrawal"
    )
    
    withdrawal_transaction = await transaction_service.create_transaction(withdrawal)
    assert withdrawal_transaction.amount == 150.0
    
    # Check final balance
    final_account = await account_service.get_account(account.account_id)
    assert final_account.balance == 550.0
    
    # Get account transactions
    transactions = await transaction_service.get_account_transactions(account.account_id)
    assert len(transactions) == 2  # deposit and withdrawal


@pytest.mark.asyncio
async def test_transfer_funds():
    """Test fund transfer between accounts."""
    # Setup dependencies
    account_repo = InMemoryAccountRepository()
    account_service = AccountService(account_repo)
    transaction_repo = InMemoryTransactionRepository()
    transaction_service = TransactionService(transaction_repo, account_service)
    
    # Create two accounts
    account1_create = AccountCreate(
        account_holder="Bob Johnson",
        account_type=AccountType.CHECKING,
        balance=1000.0
    )
    account1 = await account_service.create_account(account1_create)
    
    account2_create = AccountCreate(
        account_holder="Carol Davis",
        account_type=AccountType.SAVINGS,
        balance=500.0
    )
    account2 = await account_service.create_account(account2_create)
    
    # Transfer funds
    transfer = TransferRequest(
        from_account_id=account1.account_id,
        to_account_id=account2.account_id,
        amount=300.0,
        description="Test transfer"
    )
    
    transfer_transactions = await transaction_service.transfer_funds(transfer)
    assert len(transfer_transactions) == 2  # withdrawal and deposit
    
    # Check account balances
    account1_after = await account_service.get_account(account1.account_id)
    account2_after = await account_service.get_account(account2.account_id)
    
    assert account1_after.balance == 700.0  # 1000 - 300
    assert account2_after.balance == 800.0  # 500 + 300
    
    # Check transaction records
    account1_transactions = await transaction_service.get_account_transactions(account1.account_id)
    account2_transactions = await transaction_service.get_account_transactions(account2.account_id)
    
    assert len(account1_transactions) == 1  # withdrawal
    assert len(account2_transactions) == 1  # deposit
    
    assert account1_transactions[0].transaction_type == TransactionType.TRANSFER
    assert account2_transactions[0].transaction_type == TransactionType.TRANSFER


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_transaction_repository())
    asyncio.run(test_transaction_service())
    asyncio.run(test_transfer_funds())
    print("✅ Transaction domain tests passed!")
