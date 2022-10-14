from .database import account, engine, user, transaction
from sqlalchemy.dialects.postgresql import insert


def get_user(email):
    conn = engine.connect()
    query = user.select().where(email == user.c.email)
    return conn.execute(query).fetchone()


def get_account(owner_email):
    conn = engine.connect()
    query = account.select().where(owner_email == account.c.owner)
    return conn.execute(query).fetchone()


def add_transaction(value, account_from, account_to):
    conn = engine.connect()
    conn.execute(insert(transaction).values(value=value, account_from=account_from, account_to=account_to))


def get_transactions(email):
    conn = engine.connect()
    query = transaction.select().where(email == transaction.c.account_from)
    return conn.execute(query).fetchall()
