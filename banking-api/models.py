from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"


class AccountBase(BaseModel):
    account_holder: str
    account_type: AccountType
    balance: float = 0.0


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    account_id: str
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    amount: float
    transaction_type: TransactionType
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    account_id: str


class Transaction(TransactionBase):
    transaction_id: str
    account_id: str
    timestamp: datetime
    balance_after: float

    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float
    description: Optional[str] = None
