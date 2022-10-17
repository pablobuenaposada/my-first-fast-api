from database.database import engine
from database.models import account, user
from sqlalchemy.dialects.postgresql import insert


def populate():
    connection = engine.connect()

    # users
    user1_id = connection.execute(
        insert(user)
        .values(email="user1@example.com", password="whocares")
        .on_conflict_do_nothing()
    ).lastrowid
    user2_id = connection.execute(
        insert(user)
        .values(email="user2@example.com", password="whocares")
        .on_conflict_do_nothing()
    ).lastrowid

    # accounts
    if user1_id != 0:
        connection.execute(
            insert(account).values(owner=user1_id, balance=100).on_conflict_do_nothing()
        )
    if user2_id != 0:
        connection.execute(
            insert(account).values(owner=user2_id, balance=100).on_conflict_do_nothing()
        )
