from fastapi import FastAPI

from .crud import get_user

app = FastAPI()


@app.get("/")
def read_root():
    user = get_user("example@example.com")
    return {"Hello": user.email}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
