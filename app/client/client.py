import requests


class Requester:
    def __init__(self, url: str = "http://localhost:8000"):
        self.session = requests.Session()
        self.url = url

    def _gen_url(self, path: str):
        return f"{self.url}{path}"

    def get(self, path: str, *args, **kwargs) -> requests.Response:
        url = self._gen_url(path)
        return self.session.get(url, *args, **kwargs)

    def post(self, path: str, *args, **kwargs) -> requests.Response:
        url = self._gen_url(path)
        return self.session.post(url, *args, **kwargs)


class BusrideClient:
    def __init__(self, requestor: requests=Requester()):
        self.requests = requestor
        self.token = None

    def create_user(self, name: str, email: str, password: str):
        response = self.requests.post(
            "/users", json={"name": name, "email": email, "password": password}
        )
        return response

    def login(self, username: str, password: str):
        response = self.requests.post(
            "/login", {"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["token"]
        return response

    def query_entities(self, name: str):
        pass

    def follow_entity(self, id: str):
        pass
