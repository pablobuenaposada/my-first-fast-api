from operator import or_

from database.database import engine
from database.models import account, transaction, user
from exceptions import (AccountNotFound, NotSufficientFounds, SameAccounts,
                        UserNotFound)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound


def get_user(email):
    conn = engine.connect()
    query = user.select().where(email == user.c.email)
    try:
        return conn.execute(query).one()
    except NoResultFound:
        raise UserNotFound()


def get_account(owner_id):
    conn = engine.connect()
    query = account.select().where(owner_id == account.c.owner)
    try:
        return conn.execute(query).one()
    except NoResultFound:
        raise AccountNotFound()


def get_transaction(transaction_id):
    conn = engine.connect()
    query = transaction.select().where(transaction_id == transaction.c.id)
    return conn.execute(query).one()


def add_transaction(value, email_from, email_to):
    try:
        user_from = get_user(email_from)
    except NoResultFound:
        raise UserNotFound()

    try:
        user_to = get_user(email_to)
    except NoResultFound:
        raise UserNotFound()

    try:
        account_from = get_account(user_from.id)
    except NoResultFound:
        raise AccountNotFound()

    try:
        account_to = get_account(user_to.id)
    except NoResultFound:
        raise AccountNotFound()

    if email_from == email_to:
        raise SameAccounts()

    if account_from.balance < value:
        raise NotSufficientFounds()

    with engine.begin() as connection:
        connection.execute(
            account.update()
            .where(account.c.id == account_from.id)
            .values(balance=account.c.balance - value)
        )
        connection.execute(
            account.update()
            .where(account.c.id == account_to.id)
            .values(balance=account.c.balance + value)
        )
        result = connection.execute(
            insert(transaction).values(
                value=value, account_from=account_from.id, account_to=account_to.id
            )
        )

    return get_transaction(result.lastrowid)


def get_transactions(email):
    try:
        user = get_user(email)
    except NoResultFound:
        raise UserNotFound()
    try:
        account = get_account(user.id)
    except NoResultFound:
        raise AccountNotFound()

    conn = engine.connect()
    query = transaction.select().filter(
        or_(
            account.id == transaction.c.account_from,
            account.id == transaction.c.account_to,
        )
    )
    return conn.execute(query).fetchall()
