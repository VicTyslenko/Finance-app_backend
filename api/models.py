from datetime import datetime

from pydantic import BaseModel


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
