import os

from sqlalchemy import create_engine, event

from app.database.models import metadata_obj

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    os.getenv("DATABASE", SQLALCHEMY_DATABASE_URL),
    connect_args={"check_same_thread": False},
)
metadata_obj.create_all(engine)


# special stuff for sqlite and foreign keys
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("pragma foreign_keys=ON")


event.listen(engine, "connect", _fk_pragma_on_connect)
