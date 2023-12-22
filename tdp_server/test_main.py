from fastapi.testclient import TestClient

from tdp_server.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "tdp-server"}


def test_get_all_get_endpoints():
    response = client.get("/get-endpoints")
    assert response.status_code == 200
    assert response.json() == [
        "/api/v1/services",
        "/api/v1/services/{service_id}",
        "/api/v1/services/{service_id}/variables",
        "/api/v1/services/{service_id}/schema",
        "/api/v1/services/{service_id}/components",
        "/api/v1/services/{service_id}/components/{component_id}",
        "/api/v1/services/{service_id}/components/{component_id}/variables",
        "/api/v1/services/{service_id}/components/{component_id}/status-history",
        "/api/v1/status",
        "/api/v1/deployments",
        "/api/v1/deployments/{deployement_id}",
        "/api/v1/deployments/{deployement_id}/operations/{operation_order}/logs",
        "/api/v1/deploy/status",
        "/api/v1/validate",
        "/api/v1/operations",
        "/",
        "/get-endpoints",
    ]


def test_endpoints_response_type():
    for path in app.routes:
        response = client.get(f"{path}")
        # assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)
