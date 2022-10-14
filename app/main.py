from fastapi import FastAPI, Header, HTTPException

from .crud import add_transaction, get_account, get_transactions, get_user
from .schemas import Transaction

app = FastAPI()


def check_user(email):
    if not (user := get_user(email)):
        raise HTTPException(status_code=404, detail=f"user {email} not found")
    return user


@app.get("/account")
def account(email=Header()):
    check_user(email)
    if not (account := get_account(email)):
        raise HTTPException(status_code=404, detail="account not found")

    return {"balance": account.balance}


@app.post("/transaction", status_code=201)
def transaction_post(transaction: Transaction, email=Header()):
    check_user(email)
    check_user(transaction.account)
    add_transaction(transaction.value, email, transaction.account)
    return transaction


@app.get("/transaction")
def transaction_get(email=Header()):
    check_user(email)
    return get_transactions(email)
