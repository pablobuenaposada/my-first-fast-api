from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class Transaction(BaseModel):
    value: float
    account_to: EmailStr
