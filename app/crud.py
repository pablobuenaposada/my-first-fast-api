from operator import or_

from sqlalchemy.dialects.postgresql import insert

from .database import account, engine, transaction, user


def get_user(email):
    conn = engine.connect()
    query = user.select().where(email == user.c.email)
    return conn.execute(query).one()


def get_account(owner_email):
    conn = engine.connect()
    query = account.select().where(owner_email == account.c.owner)
    return conn.execute(query).one()


def add_transaction(value, user_from, user_to):
    conn = engine.connect()
    conn.execute(
        insert(transaction).values(
            value=value, account_from=user_from.id, account_to=user_to.id
        )
    )


def get_transactions(user):
    conn = engine.connect()
    query = transaction.select().filter(
        or_(user.id == transaction.c.account_from, user.id == transaction.c.account_to)
    )
    return conn.execute(query).fetchall()
