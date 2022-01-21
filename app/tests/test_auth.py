from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_ping():
    respose = client.get("/ping")
    assert respose.status_code == 401


def test_login_success():
    # TODO: setup test database and create fixtures to clear and populate with test data
    # await User.create(name='Test2', email='test@gmail.com', password='a')
    response = client.post(
        "/login", data={"username": "test@gmail.com", "password": "a"}
    )
    assert response.status_code == 200
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/ping", headers=headers)
    assert response.status_code == 200
