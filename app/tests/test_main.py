from decimal import Decimal

from fastapi.testclient import TestClient

from app.crud import get_account
from app.database.database import engine
from app.main import app
from app.tests.utils import create_account, create_transaction, create_user

client = TestClient(app)


class TestGetAccount:
    URL = "/account"
    EMAIL = "whatever@gmail.com"

    def test_success(self):
        user_id = create_user(self.EMAIL)
        create_account(user_id)
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 200
        assert response.json() == {"id": user_id, "balance": 0.0}

    def test_no_account(self):
        create_user(self.EMAIL)
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 404
        assert response.json() == {"detail": "account not found"}

    def test_no_user(self):
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 404
        assert response.json() == {"detail": f"user {self.EMAIL} not found"}

    def test_no_headers(self):
        response = client.get(self.URL)

        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["header", "email"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }


class TestGetTransaction:
    URL = "/transaction"
    EMAIL = "whatever@gmail.com"
    VALUE = 100

    def test_success(self):
        user1_id = create_user(self.EMAIL)
        user2_id = create_user("whatever2@gmail.com")
        account1_id = create_account(user1_id)
        account2_id = create_account(user2_id)
        transaction_id = create_transaction(self.VALUE, account1_id, account2_id)
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 200
        assert response.json() == [
            {
                "id": transaction_id,
                "value": self.VALUE,
                "account_from": account1_id,
                "account_to": account2_id,
                "created": response.json()[0]["created"],
            }
        ]

    def test_no_transactions(self):
        user_id = create_user(self.EMAIL)
        create_account(user_id)
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 200
        assert response.json() == []

    def test_no_account(self):
        create_user(self.EMAIL)
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 404
        assert response.json() == {"detail": "account not found"}

    def test_no_user(self):
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 404
        assert response.json() == {"detail": f"user {self.EMAIL} not found"}

    def test_no_headers(self):
        response = client.get(self.URL)

        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["header", "email"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }


class TestPostTransaction:
    URL = "/transaction"
    EMAIL1 = "whatever@gmail.com"
    EMAIL2 = "whatever2@gmail.com"
    VALUE = 100

    def test_success(self):
        user1_id = create_user(self.EMAIL1)
        user2_id = create_user(self.EMAIL2)
        account1_id = create_account(user1_id, 300)
        account2_id = create_account(user2_id)

        assert get_account(account1_id).balance == Decimal(300)
        assert get_account(account2_id).balance == Decimal(0)

        response = client.post(
            self.URL,
            json={"value": self.VALUE, "email": self.EMAIL2},
            headers={"email": self.EMAIL1},
        )

        assert response.status_code == 201
        assert response.json() == {"value": self.VALUE, "email": self.EMAIL2}
        assert get_account(account1_id).balance == Decimal(200)
        assert get_account(account2_id).balance == Decimal(100)
