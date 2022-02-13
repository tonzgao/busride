from fastapi.testclient import TestClient

from ..main import app
from ..client.client import BusrideClient

client = BusrideClient(TestClient(app))


def test_ping():
    respose = client.requests.get("/ping")
    assert respose.status_code == 401


def test_login_success():
    try:
        client.create_user("Test", "test@gmail.com", "password")
    except:
        pass
    response = client.login("test@gmail.com", "password")
    assert response.status_code == 200
    token = client.token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.requests.get("/ping", headers=headers)
    assert response.status_code == 200
