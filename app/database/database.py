from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

from app.database.models import metadata_obj, user, account

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata_obj.create_all(engine)
conn = engine.connect()

### crap for foreing keys
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("pragma foreign_keys=ON")


from sqlalchemy import event

event.listen(engine, "connect", _fk_pragma_on_connect)

########################

conn.execute(
    insert(user)
    .values(email="example@example.com", password="aaaa")
    .on_conflict_do_nothing()
)
conn.execute(
    insert(user)
    .values(email="example2@example.com", password="aaaa")
    .on_conflict_do_nothing()
)

conn.execute(insert(account).values(owner=1, balance=100).on_conflict_do_nothing())
conn.execute(insert(account).values(owner=2, balance=100).on_conflict_do_nothing())
