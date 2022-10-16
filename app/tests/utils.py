from sqlalchemy.dialects.postgresql import insert

from app.database.database import engine
from app.database.models import account, user


def create_user(email, password="whatever"):
    connection = engine.connect()
    connection.execute(insert(user).values(email=email, password=password))


def create_account(balance=0):
    connection = engine.connect()
    connection.execute(insert(account).values(owner=1, balance=balance))
