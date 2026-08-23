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