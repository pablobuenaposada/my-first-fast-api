from pydantic.main import BaseModel


class Account(BaseModel):
    id: int
    owner: int
    balance: int
