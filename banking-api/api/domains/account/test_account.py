import pytest
import asyncio
from datetime import datetime
from .models import Account, AccountCreate, AccountType
from .memory_repository import InMemoryAccountRepository
from .service import AccountService


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
async def test_account_service():
    """Test account service operations."""
    account_repo = InMemoryAccountRepository()
    service = AccountService(account_repo)
    
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
    assert created_account.is_active == True
    
    # Get account
    retrieved_account = await service.get_account(account_id)
    assert retrieved_account.account_holder == "Alice Smith"
    
    # Update account
    account_update = AccountCreate(
        account_holder="Alice Johnson",
        account_type=AccountType.CHECKING,
        balance=500.0  # Balance should remain the same
    )
    
    updated_account = await service.update_account(account_id, account_update)
    assert updated_account.account_holder == "Alice Johnson"
    assert updated_account.account_type == AccountType.CHECKING
    assert updated_account.balance == 500.0  # Balance preserved
    
    # Get all accounts
    all_accounts = await service.get_all_accounts()
    assert len(all_accounts) == 1
    
    # Delete account
    await service.delete_account(account_id)
    active_accounts = await service.get_all_accounts()
    assert len(active_accounts) == 0  # Should be empty after soft delete


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_account_repository())
    asyncio.run(test_account_service())
    print("✅ Account domain tests passed!")
