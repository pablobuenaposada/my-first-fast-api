from operator import or_

from sqlalchemy.dialects.postgresql import insert

from .database.database import engine
from .database.models import account, transaction, user
from .exceptions import NotSufficientFounds


def get_user(email):
    conn = engine.connect()
    query = user.select().where(email == user.c.email)
    return conn.execute(query).one()


def get_account(owner):
    conn = engine.connect()
    query = account.select().where(owner == account.c.owner)
    return conn.execute(query).one()


def add_transaction(value, user_from_id, user_to_id):
    account_from = get_account(user_from_id)
    if account_from.balance < value:
        raise NotSufficientFounds()

    with engine.begin() as connection:
        connection.execute(
            account.update()
            .where(account.c.id == user_from_id)
            .values(balance=account.c.balance - value)
        )
        connection.execute(
            account.update()
            .where(account.c.id == user_to_id)
            .values(balance=account.c.balance + value)
        )
        connection.execute(
            insert(transaction).values(
                value=value, account_from=user_from_id, account_to=user_to_id
            )
        )


def get_transactions(user):
    conn = engine.connect()
    query = transaction.select().filter(
        or_(user.id == transaction.c.account_from, user.id == transaction.c.account_to)
    )
    return conn.execute(query).fetchall()
