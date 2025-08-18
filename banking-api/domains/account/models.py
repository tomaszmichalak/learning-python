from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


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
