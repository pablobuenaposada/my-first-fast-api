from datetime import datetime

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, Numeric, Table,
                        create_engine)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils import EmailType, PasswordType

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

metadata_obj = MetaData()
user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("email", EmailType, nullable=False, unique=True),
    Column("password", PasswordType(schemes=["pbkdf2_sha512"]), nullable=False),
)
account = Table(
    "account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("owner", EmailType, ForeignKey("user.email"), nullable=False, unique=True),
    Column("balance", Numeric(scale=2), default=0, nullable=False),
)
transaction = Table(
    "transaction",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("value", Numeric(scale=2), nullable=False),
    Column("account_from", Integer, ForeignKey("account.id"), nullable=False),
    Column("account_to", Integer, ForeignKey("account.id"), nullable=False),
    Column(
        "created", TIMESTAMP(timezone=False), nullable=False, default=datetime.now()
    ),
)
metadata_obj.create_all(engine)
conn = engine.connect()

conn.execute(
    insert(user)
    .values(email="example@example.com", password="aaaa")
    .on_conflict_do_nothing()
)

conn.execute(
    insert(account).values(owner="example@example.com").on_conflict_do_nothing()
)


from sqlalchemy import func, select

count = conn.execute(
    select(func.count()).select_from(select(account).subquery())
).scalar_one()


print(count)
