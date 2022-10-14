from fastapi import FastAPI, Header, HTTPException

from .crud import add_transaction, get_account, get_transactions, get_user
from .schemas import Transaction

app = FastAPI()


@app.get("/account")
def account(email=Header(default=None)):
    if not (user := get_user(email)):
        raise HTTPException(status_code=404, detail="user not found")
    if not (account := get_account(user.email)):
        raise HTTPException(status_code=404, detail="account not found")

    return {"balance": account.balance}


@app.post("/transaction")
def transaction(transaction: Transaction, email=Header(default=None)):
    add_transaction(transaction.value, email, transaction.account_to)
    return transaction


@app.get("/transaction")
def transaction2(email=Header(default=None)):
    return get_transactions(email)
