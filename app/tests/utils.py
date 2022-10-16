from sqlalchemy.dialects.postgresql import insert

from app.database.database import engine
from app.database.models import account, transaction, user


def create_user(email, password="whatever"):
    connection = engine.connect()
    result = connection.execute(insert(user).values(email=email, password=password))
    return result.lastrowid


def create_account(owner, balance=0):
    connection = engine.connect()
    result = connection.execute(insert(account).values(owner=owner, balance=balance))
    return result.lastrowid


def create_transaction(value, account_from, account_to):
    connection = engine.connect()
    result = connection.execute(
        insert(transaction).values(
            value=value, account_from=account_from, account_to=account_to
        )
    )
    return result.lastrowid
