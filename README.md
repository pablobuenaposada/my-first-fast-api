# My first FastAPI project

## Constraints
* Not use any ORM, sqlalchemy is fine but without ORM
* Only one bank account per email
* Python 3.9

## Run the project (with Docker)
Do:

`make docker/build`

`make docker/run`

project will live in `http://localhost/` (port 80)

you should get a 404 with that url in your browser:
```
{"detail":"Not Found"}
```

## Endpoints
Documentation is available in `http://localhost/docs` but there's a simple explanation in here:

The project comes pre-populated with 2 users (user1@example.com and user2@example.com) and each user has its own bank account, the email acts as authentication token to make it simpler,
so you need to send the email within the headers so the system knows who you are.

Every account starts with a balance of 100.00 (sorry, no currency implemented)

### `GET /account` retrieve account details
    ```
    curl --request GET --url http://localhost/account --header 'email: user1@example.com'
    {
        "id":2,
        "owner":1,
        "balance":100.0
    }
    ```

### `POST /transaction` send money
example of sending 10 from user1@example.com account to user2@example.com

    ```
    curl --request POST --url http://localhost/transaction --header 'email: user1@example.com' --data '{"value": 10, "email": "user2@example.com"}'
    {
        "id": 1,
        "value": 10.0,
        "account_from": 2,
        "account_to": 1,
        "created": "2022-10-17T21:18:05.154850"
    }
    ```

### `GET /transaction` retrieve account transactions
    ```
    curl --request GET --url http://localhost/transaction --header 'email: user1@example.com'
    [
        {
            "id": 1,
            "value": 10.0,
            "account_from": 2,
            "account_to": 1,
            "created": "2022-10-17T21:18:05.154850"
        },
        {
            "id": 2,
            "value": 33.0,
            "account_from": 1,
            "account_to": 2,
            "created": "2022-10-17T21:18:05.154850"
        }
    ]
    ```

## Run tests
I haven't had time to make the test to run through docker, so in this case, they are going to be run locally with a virtual env.

Just do: `make tests`
```
python3.9 -m venv venv
venv/bin/pip install -r requirements.txt
Collecting SQLAlchemy
  Using cached SQLAlchemy-1.4.42.tar.gz (8.3 MB)
  Preparing metadata (setup.py) ... done
Collecting SQLAlchemy-Utils
  ...
Installing collected packages: mypy-extensions, iniconfig, urllib3, tomli, pyparsing, py, pluggy, platformdirs, pathspec, isort, charset-normalizer, certifi, attrs, requests, packaging, black, pytest
Successfully installed attrs-22.1.0 black-22.10.0 certifi-2022.9.24 charset-normalizer-2.1.1 iniconfig-1.1.1 isort-5.10.1 mypy-extensions-0.4.3 packaging-21.3 pathspec-0.10.1 platformdirs-2.5.2 pluggy-1.0.0 py-1.11.0 pyparsing-3.0.9 pytest-7.1.3 requests-2.28.1 tomli-2.0.1 urllib3-1.26.12
DATABASE=sqlite:///./test.db PYTHONPATH=app venv/bin/pytest app/tests
================================================================= test session starts ==================================================================
platform darwin -- Python 3.9.14, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/pablobuenaposadasanchez/Desktop/my-first-fast-api
plugins: anyio-3.6.1
collected 13 items

app/tests/test_main.py .............                                                                                                             [100%]

=================================================================== warnings summary ===================================================================
app/tests/test_main.py::TestGetAccount::test_success
  /Users/pablobuenaposadasanchez/Desktop/my-first-fast-api/app/crud.py:20: SAWarning: Dialect sqlite+pysqlite does *not* support Decimal objects natively, and SQLAlchemy must convert from floating point - rounding errors and other issues may occur. Please consider storing Decimal numbers as strings or integers on this platform for lossless storage.
    return conn.execute(query).one()

app/tests/test_main.py::TestGetTransaction::test_success
  /Users/pablobuenaposadasanchez/Desktop/my-first-fast-api/app/crud.py:93: SAWarning: Dialect sqlite+pysqlite does *not* support Decimal objects natively, and SQLAlchemy must convert from floating point - rounding errors and other issues may occur. Please consider storing Decimal numbers as strings or integers on this platform for lossless storage.
    return conn.execute(query).fetchall()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================ 13 passed, 2 warnings in 2.41s ============================================================
```