from .database import engine, user


def get_user(email):
    conn = engine.connect()
    query = user.select().where(email == user.c.email)
    result = conn.execute(query)
    return result.fetchone()
