from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    email: str
    full_name: str
    created_at: datetime
    avatar_url:str | None = None

class Counterparty(BaseModel):
   counterparty_id:int
   name:str
   slug:str
   avatar_url:str | None = None
   kind:str
   created_at: datetime

class Transaction(BaseModel):
    """A ledger row joined to its counterparty, shaped for the UI."""

    transaction_id: int
    counterparty: str
    counterparty_slug: str
    avatar_url: str
    category: str
    amount: float  # float, not Decimal: Pydantic serialises Decimal as a JSON string
    occurred_at: datetime

class BudgetCreate(BaseModel):
    """What the client sends to create a budget."""

    category: str
    maximum_spend: Decimal = Field(gt=0, max_digits=12,      decimal_places=2)
    theme: str

class Budget(BaseModel):
    """A budget row as returned to the UI."""

    budget_id: int
    category: str
    maximum_spend: float # float, not Deccimal - same reason as Transaction.amount
    theme: str
    created_at: datetime 