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
    return {"id": account.id, "balance": account.balance}


@app.get("/transaction")
def transaction_get(email=Header()):
    # pagination?
    user = check_user(email)
    return get_transactions(user)


@app.post("/transaction", status_code=201)
def transaction_post(transaction: Transaction, email=Header()):
    if email == transaction.email:
        raise HTTPException(status_code=400, detail="origin and destination accounts (emails) are the same")
    user_from = check_user(email)
    user_to = check_user(transaction.email)
    add_transaction(transaction.value, user_from, user_to)
    return transaction
