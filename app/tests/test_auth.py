from fastapi.testclient import TestClient

from ..main import app
from ..client.client import BusrideClient

client = BusrideClient(TestClient(app))


def test_ping():
    respose = client.requests.get("/whoami")
    assert respose.status_code == 401


def test_login_success():
    try:
        client.create_user("Test", "test@gmail.com", "password")
    except:
        pass
    response = client.login("test@gmail.com", "password")
    assert response.status_code == 200
    assert client.token is not None
    response = client.requests.get("/whoami", headers=client._gen_auth_headers())
    assert response.status_code == 200
