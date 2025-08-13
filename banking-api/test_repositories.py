import pytest
import asyncio
from datetime import datetime
from models import Account, AccountCreate, Transaction, TransactionCreate, TransferRequest, AccountType, TransactionType
from memory_repository import InMemoryAccountRepository, InMemoryTransactionRepository
from services import BankingService


@pytest.mark.asyncio
async def test_account_repository():
    """Test account repository operations."""
    repo = InMemoryAccountRepository()
    
    # Create account
    account = Account(
        account_id="test-123",
        account_holder="John Doe",
        account_type=AccountType.CHECKING,
        balance=1000.0,
        created_at=datetime.now(),
        is_active=True
    )
    
    created_account = await repo.create_account(account)
    assert created_account.account_id == "test-123"
    assert created_account.account_holder == "John Doe"
    
    # Get account
    retrieved_account = await repo.get_account("test-123")
    assert retrieved_account is not None
    assert retrieved_account.account_holder == "John Doe"
    
    # Account exists
    assert await repo.account_exists("test-123") == True
    assert await repo.account_exists("non-existent") == False
    
    # Get all accounts
    all_accounts = await repo.get_all_accounts()
    assert len(all_accounts) == 1
    
    # Update account
    account.balance = 1500.0
    updated_account = await repo.update_account(account)
    assert updated_account.balance == 1500.0
    
    # Delete account (soft delete)
    await repo.delete_account("test-123")
    active_accounts = await repo.get_all_accounts()
    assert len(active_accounts) == 0  # Should return only active accounts


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
async def test_banking_service():
    """Test banking service operations."""
    account_repo = InMemoryAccountRepository()
    transaction_repo = InMemoryTransactionRepository()
    service = BankingService(account_repo, transaction_repo)
    
    # Create account
    account_create = AccountCreate(
        account_holder="Alice Smith",
        account_type=AccountType.SAVINGS,
        balance=500.0
    )
    
    created_account = await service.create_account(account_create)
    account_id = created_account.account_id
    assert created_account.account_holder == "Alice Smith"
    assert created_account.balance == 500.0
    
    # Create deposit transaction
    deposit = TransactionCreate(
        account_id=account_id,
        amount=200.0,
        transaction_type=TransactionType.DEPOSIT,
        description="Test deposit"
    )
    
    deposit_transaction = await service.create_transaction(deposit)
    assert deposit_transaction.amount == 200.0
    
    # Check account balance updated
    updated_account = await service.get_account(account_id)
    assert updated_account.balance == 700.0
    
    # Create withdrawal transaction
    withdrawal = TransactionCreate(
        account_id=account_id,
        amount=100.0,
        transaction_type=TransactionType.WITHDRAWAL,
        description="Test withdrawal"
    )
    
    withdrawal_transaction = await service.create_transaction(withdrawal)
    assert withdrawal_transaction.amount == 100.0
    
    # Check final balance
    final_account = await service.get_account(account_id)
    assert final_account.balance == 600.0
    
    # Get account transactions
    transactions = await service.get_account_transactions(account_id)
    assert len(transactions) == 2  # deposit and withdrawal


@pytest.mark.asyncio
async def test_transfer_funds():
    """Test fund transfer between accounts."""
    account_repo = InMemoryAccountRepository()
    transaction_repo = InMemoryTransactionRepository()
    service = BankingService(account_repo, transaction_repo)
    
    # Create two accounts
    account1_create = AccountCreate(
        account_holder="Bob Johnson",
        account_type=AccountType.CHECKING,
        balance=1000.0
    )
    account1 = await service.create_account(account1_create)
    
    account2_create = AccountCreate(
        account_holder="Carol Davis",
        account_type=AccountType.SAVINGS,
        balance=500.0
    )
    account2 = await service.create_account(account2_create)
    
    # Transfer funds
    transfer = TransferRequest(
        from_account_id=account1.account_id,
        to_account_id=account2.account_id,
        amount=300.0,
        description="Test transfer"
    )
    
    transfer_transactions = await service.transfer_funds(transfer)
    assert len(transfer_transactions) == 2  # withdrawal and deposit
    
    # Check account balances
    account1_after = await service.get_account(account1.account_id)
    account2_after = await service.get_account(account2.account_id)
    
    assert account1_after.balance == 700.0  # 1000 - 300
    assert account2_after.balance == 800.0  # 500 + 300


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_account_repository())
    asyncio.run(test_transaction_repository())
    asyncio.run(test_banking_service())
    asyncio.run(test_transfer_funds())
    print("All tests passed!")
