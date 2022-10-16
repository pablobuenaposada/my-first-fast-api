from fastapi.testclient import TestClient

from app.main import app
from app.tests.utils import create_account, create_user

client = TestClient(app)


class TestGetAccount:
    URL = "/account"
    EMAIL = "whatever@gmail.com"

    def test_success(self):
        create_user(self.EMAIL)
        create_account()
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 200
        assert response.json() == {"id": 1, "balance": 0.0}

    def test_no_account(self):
        create_user(self.EMAIL)
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 404
        assert response.json() == {"detail": "account not found"}

    def test_no_user(self):
        response = client.get(self.URL, headers={"email": self.EMAIL})

        assert response.status_code == 404
        assert response.json() == {"detail": "user not found"}

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
