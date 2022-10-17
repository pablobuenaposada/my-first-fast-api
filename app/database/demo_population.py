from database.database import engine
from database.models import account, user
from sqlalchemy.dialects.postgresql import insert


def populate():
    connection = engine.connect()

    # users
    connection.execute(
        insert(user)
        .values(email="example@example.com", password="aaaa")
        .on_conflict_do_nothing()
    )
    connection.execute(
        insert(user)
        .values(email="example2@example.com", password="aaaa")
        .on_conflict_do_nothing()
    )

    # accounts
    connection.execute(
        insert(account).values(owner=1, balance=100).on_conflict_do_nothing()
    )
    connection.execute(
        insert(account).values(owner=2, balance=100).on_conflict_do_nothing()
    )
