import os

from crud import (add_transaction, add_user_and_account, get_account,
                  get_transactions, get_user)
from database.demo_population import populate
from exceptions import (AccountNotFound, NotSufficientFounds, SameAccounts,
                        UserAlreadyIn, UserNotFound)
from fastapi import FastAPI, Header, HTTPException
from schemas import AccountIn, AccountOut, TransactionIn, TransactionOut

app = FastAPI()


@app.on_event("startup")
def startup_event():
    if "TEST" in os.environ:
        populate()


@app.get("/account", response_model=AccountOut)
def account_get(email=Header()):
    try:
        user = get_user(email)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)
    try:
        account = get_account(user.id)
    except AccountNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)

    return account


@app.post("/account", status_code=201, response_model=AccountOut)
def account_post(account: AccountIn):
    """Both user and account would be created by this endpoint"""
    try:
        return add_user_and_account(account.email, account.password, account.balance)
    except UserAlreadyIn as error:
        raise HTTPException(status_code=409, detail=error.message)


@app.get("/transaction")
def transaction_get(email=Header()):
    # would be nice to use pagination
    try:
        return get_transactions(email)
    except AccountNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)


@app.post("/transaction", status_code=201, response_model=TransactionOut)
def transaction_post(transaction: TransactionIn, email=Header()):
    try:
        return add_transaction(transaction.value, email, transaction.email)
    except NotSufficientFounds as error:
        raise HTTPException(
            status_code=400,
            detail=error.message,
        )
    except SameAccounts as error:
        raise HTTPException(
            status_code=400,
            detail=error.message,
        )
    except AccountNotFound as error:
        raise HTTPException(status_code=400, detail=error.message)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)
