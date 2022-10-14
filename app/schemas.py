from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import PositiveFloat


class Transaction(BaseModel):
    value: PositiveFloat
    account: EmailStr
