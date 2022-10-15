from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import PositiveFloat


class TransactionIn(BaseModel):
    value: PositiveFloat
    email: EmailStr
