from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, MetaData, Numeric, Table
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils import EmailType, PasswordType

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("email", EmailType, nullable=False, unique=True),
    Column(
        "password", PasswordType(schemes=["pbkdf2_sha512"]), nullable=False
    ),  # not used actually
)
account = Table(
    "account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("owner", Integer, ForeignKey("user.id"), nullable=False, unique=True),
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
