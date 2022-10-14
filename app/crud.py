from sqlalchemy.dialects.postgresql import insert

from .database import account, engine, transaction, user


def get_user(email):
    conn = engine.connect()
    query = user.select().where(email == user.c.email)
    return conn.execute(query).fetchone()


def get_account(owner_email):
    conn = engine.connect()
    query = account.select().where(owner_email == account.c.owner)
    return conn.execute(query).fetchone()


def add_transaction(value, user_from, user_to):
    conn = engine.connect()
    conn.execute(
        insert(transaction).values(
            value=value, account_from=user_from.id, account_to=user_to.id
        )
    )


def get_transactions(user):
    conn = engine.connect()
    query = transaction.select().where(user.id == transaction.c.account_from)
    return conn.execute(query).fetchall()
