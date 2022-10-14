from typing import Union

from fastapi import FastAPI, Header, Request

from .crud import get_account, get_user, add_transaction, get_transactions
from pydantic import BaseModel

app = FastAPI()


class Transaction(BaseModel):
    value: float
    account_from: str
    account_to: str


# @app.get("/")
# def read_root():
#     user = get_user("example@example.com")
#     account = get_account(user.email)
#     return {"Hello": account.balance}

# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.get("/account")
def account(email=Header(default=None)):
    account = get_account(get_user(email).email)
    return {"balance": account.balance}


@app.post("/transaction")
def transaction(transaction: Transaction, email=Header(default=None)):
    add_transaction(transaction.value, transaction.account_from, transaction.account_to)
    return transaction


@app.get("/transaction")
def transaction2(email=Header(default=None)):
    return get_transactions(email)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
