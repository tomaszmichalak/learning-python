import pytest
import asyncio
from datetime import datetime

# Account domain imports
from domains.account.models import Account, AccountCreate, AccountType
from domains.account.memory_repository import InMemoryAccountRepository
from domains.account.service import AccountService

# Transaction domain imports
from domains.transaction.models import Transaction, TransactionCreate, TransferRequest, TransactionType
from domains.transaction.memory_repository import InMemoryTransactionRepository
from domains.transaction.service import TransactionService


@pytest.mark.asyncio
async def test_account_domain():
    """Test account domain functionality."""
    # Setup
    account_repo = InMemoryAccountRepository()
    account_service = AccountService(account_repo)
    
    # Create account
    account_create = AccountCreate(
        account_holder="John Doe",
        account_type=AccountType.CHECKING,
        balance=1000.0
    )
    
    created_account = await account_service.create_account(account_create)
    assert created_account.account_holder == "John Doe"
    assert created_account.balance == 1000.0
    assert created_account.is_active == True
    
    # Get account
    retrieved_account = await account_service.get_account(created_account.account_id)
    assert retrieved_account.account_holder == "John Doe"
    
    # Update account
    account_update = AccountCreate(
        account_holder="John Smith",
        account_type=AccountType.SAVINGS,
        balance=1000.0  # Balance should remain the same
    )
    
    updated_account = await account_service.update_account(created_account.account_id, account_update)
    assert updated_account.account_holder == "John Smith"
    assert updated_account.account_type == AccountType.SAVINGS
    assert updated_account.balance == 1000.0  # Balance preserved
    
    # Get all accounts
    all_accounts = await account_service.get_all_accounts()
    assert len(all_accounts) == 1
    
    # Delete account
    await account_service.delete_account(created_account.account_id)
    active_accounts = await account_service.get_all_accounts()
    assert len(active_accounts) == 0  # Should be empty after soft delete


@pytest.mark.asyncio
async def test_transaction_domain():
    """Test transaction domain functionality."""
    # Setup
    account_repo = InMemoryAccountRepository()
    account_service = AccountService(account_repo)
    transaction_repo = InMemoryTransactionRepository()
    transaction_service = TransactionService(transaction_repo, account_service)
    
    # Create account first
    account_create = AccountCreate(
        account_holder="Alice Johnson",
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
    assert len(transactions) == 2


@pytest.mark.asyncio
async def test_transfer_between_accounts():
    """Test fund transfer between accounts."""
    # Setup
    account_repo = InMemoryAccountRepository()
    account_service = AccountService(account_repo)
    transaction_repo = InMemoryTransactionRepository()
    transaction_service = TransactionService(transaction_repo, account_service)
    
    # Create two accounts
    account1_create = AccountCreate(
        account_holder="Bob Wilson",
        account_type=AccountType.CHECKING,
        balance=1000.0
    )
    account1 = await account_service.create_account(account1_create)
    
    account2_create = AccountCreate(
        account_holder="Carol Davis",
        account_type=AccountType.SAVINGS,
        balance=300.0
    )
    account2 = await account_service.create_account(account2_create)
    
    # Transfer funds
    transfer = TransferRequest(
        from_account_id=account1.account_id,
        to_account_id=account2.account_id,
        amount=250.0,
        description="Test transfer"
    )
    
    transfer_transactions = await transaction_service.transfer_funds(transfer)
    assert len(transfer_transactions) == 2  # withdrawal and deposit
    
    # Check account balances
    account1_after = await account_service.get_account(account1.account_id)
    account2_after = await account_service.get_account(account2.account_id)
    
    assert account1_after.balance == 750.0  # 1000 - 250
    assert account2_after.balance == 550.0  # 300 + 250
    
    # Check transaction records
    account1_transactions = await transaction_service.get_account_transactions(account1.account_id)
    account2_transactions = await transaction_service.get_account_transactions(account2.account_id)
    
    assert len(account1_transactions) == 1  # withdrawal
    assert len(account2_transactions) == 1  # deposit
    
    assert account1_transactions[0].transaction_type == TransactionType.TRANSFER
    assert account2_transactions[0].transaction_type == TransactionType.TRANSFER


@pytest.mark.asyncio
async def test_domain_separation():
    """Test that domains are properly separated."""
    # Account domain should work independently
    account_repo = InMemoryAccountRepository()
    account_service = AccountService(account_repo)
    
    account_create = AccountCreate(
        account_holder="Test User",
        account_type=AccountType.CHECKING,
        balance=100.0
    )
    
    account = await account_service.create_account(account_create)
    assert account.account_holder == "Test User"
    
    # Transaction domain depends on account domain (as expected)
    transaction_repo = InMemoryTransactionRepository()
    transaction_service = TransactionService(transaction_repo, account_service)
    
    transaction_create = TransactionCreate(
        account_id=account.account_id,
        amount=50.0,
        transaction_type=TransactionType.DEPOSIT,
        description="Domain separation test"
    )
    
    transaction = await transaction_service.create_transaction(transaction_create)
    assert transaction.amount == 50.0
    assert transaction.account_id == account.account_id


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_account_domain())
    asyncio.run(test_transaction_domain())
    asyncio.run(test_transfer_between_accounts())
    asyncio.run(test_domain_separation())
    print("🎉 All domain tests passed!")
