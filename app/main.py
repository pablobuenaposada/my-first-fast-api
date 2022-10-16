import os

from fastapi import FastAPI, Header, HTTPException
from sqlalchemy.orm.exc import NoResultFound

from .crud import add_transaction, get_account, get_transactions, get_user
from .database.demo_population import populate
from .exceptions import AccountNotFound, NotSufficientFounds
from .schemas import TransactionIn

app = FastAPI()


def check_user(email):
    try:
        user = get_user(email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"user {email} not found")
    return user


def check_account(owner_id):
    try:
        account = get_account(owner_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"account not found")
    return account


@app.on_event("startup")
def startup_event():
    if "TEST" in os.environ:
        populate()


@app.get("/account")
def account(email=Header()):
    user = check_user(email)
    account = check_account(user.id)
    return {"id": account.id, "balance": account.balance}


@app.get("/transaction")
def transaction_get(email=Header()):
    # pagination?
    user = check_user(email)
    check_account(user.id)

    return get_transactions(user)


@app.post("/transaction", status_code=201)
def transaction_post(transaction: TransactionIn, email=Header()):
    if email == transaction.email:
        raise HTTPException(
            status_code=400,
            detail="origin and destination accounts (emails) are the same",
        )
    user_from = check_user(email)
    user_to = check_user(transaction.email)
    try:
        add_transaction(transaction.value, user_from.id, user_to.id)
    except NotSufficientFounds:
        raise HTTPException(
            status_code=400,
            detail=f"account from {email} doesn't have sufficient founds",
        )
    except AccountNotFound:
        raise HTTPException(
            status_code=400,
            detail=f"account from {email} not founds",
        )
    return transaction
