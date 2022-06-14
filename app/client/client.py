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
    def __init__(self, requestor: requests = Requester()):
        self.requests = requestor
        self.token = None

    def _gen_auth_headers(self):
        if not self.token:
            raise Exception("Not logged in")
        return {"Authorization": f"Bearer {self.token}"}

    def create_user(self, name: str, email: str, password: str):
        response = self.requests.post(
            "/users", json={"name": name, "email": email, "password": password}
        )
        return response

    def add_api(self, name, data):
        return self.requests.post(
            "/apis",
            json={"name": name, "data": data},
            headers=self._gen_auth_headers(),
        )

    def login(self, username: str, password: str):
        response = self.requests.post(
            "/login", {"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["token"]
        return response

    def follow_match(self, name: str):
        entities = self.query_entities(name)
        entity = entities["search"][0]
        if not entity:
            raise Exception("Not found")
        self.follow_entity(entity["id"])
        return entity

    def query_entities(self, name: str):
        return self.requests.get(f"/entities/tags/{name}").json()

    def follow_entity(self, id: str):
        entity = self.requests.get(f"/entities/tag/{id}").json()
        if not entity:
            entity = self.requests.post(
                f"/entities", json={"identifier": id}
            ).json()
        response = self.requests.post(
            "/interests",
            json={"entity_id": entity["id"],},
            headers=self._gen_auth_headers(),
        )
        return response

    def debug_entity(self, id: str):
        return self.requests.post(f"/entities/{id}/force_check").json()
