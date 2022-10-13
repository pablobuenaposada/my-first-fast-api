from sqlalchemy import (Column, ForeignKey, Integer, MetaData, Table,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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
    Column("email", EmailType, primary_key=True),
    Column("password", PasswordType(schemes=["pbkdf2_sha512"]), nullable=False),
)

account = Table(
    "account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("owner", EmailType, ForeignKey("user.email")),
)
# transaction = Table("transaction", metadata_obj, Column("id", Integer, primary_key=True))
metadata_obj.create_all(engine)

stmt = user.insert().values(email="example@example.com", password="aaaa")
conn = engine.connect()
conn.execute(stmt)
print(stmt)
