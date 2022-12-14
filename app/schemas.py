from datetime import datetime

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import PositiveFloat


def max_2_decimals(value):
    if len(str(value).split(".")[1]) > 2:
        raise ValueError("No more than 2 decimals allowed")
    return value


class TransactionIn(BaseModel):
    value: PositiveFloat
    email: EmailStr

    @validator("value")
    def validate_value(cls, value):
        return max_2_decimals(value)


class TransactionOut(BaseModel):
    id: int
    value: float
    account_from: int
    account_to: int
    created: datetime


class AccountIn(BaseModel):
    email: EmailStr
    password: str
    balance: PositiveFloat

    @validator("balance")
    def validate_value(cls, value):
        return max_2_decimals(value)


class AccountOut(BaseModel):
    id: int
    owner: int
    balance: float
