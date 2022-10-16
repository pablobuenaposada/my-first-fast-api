from datetime import datetime

from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import PositiveFloat


class TransactionIn(BaseModel):
    value: PositiveFloat(decimal_places=2)
    email: EmailStr


class TransactionOut(BaseModel):
    id: int
    value: float
    account_from: int
    account_to: int
    created: datetime


class AccountOut(BaseModel):
    id: int
    owner: int
    balance: float
