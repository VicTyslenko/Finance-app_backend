from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    email: str
    full_name: str
    created_at: datetime
