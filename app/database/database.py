from sqlalchemy import create_engine

from app.database.models import account, metadata_obj, user

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
