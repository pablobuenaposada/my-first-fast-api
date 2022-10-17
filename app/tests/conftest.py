import contextlib

import pytest
from database.database import engine
from database.models import metadata_obj


@pytest.fixture(autouse=True)
def truncate_tables():
    """this function deletes all records in the database so every test starts fresh"""
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata_obj.sorted_tables):
            con.execute(table.delete())
        trans.commit()
