from fastapi.testclient import TestClient

from tdp_server.main import app

client = TestClient(app)


def test_get_all_get_endpoints():
    response = client.get("/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_endpoints_response_type():
    for path in app.routes:
        response = client.get(f"{path}")
        # assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)
