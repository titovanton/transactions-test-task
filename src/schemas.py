from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from models import Transaction


class SortField(str, Enum):
    email = 'user_email'
    nickname = 'user_nickname'
    date = 'transaction_date'
    status = 'transaction_status'


class SortOrder(str, Enum):
    asc = 'asc'
    desc = 'desc'


class RootResponse(BaseModel):
    user_nickname: str
    user_email: str
    card_id: int
    card_mask_number: str
    card_balance: float
    transaction_id: int
    transaction_date: datetime
    transaction_amount: float
    transaction_status: Transaction.StatusChoices
