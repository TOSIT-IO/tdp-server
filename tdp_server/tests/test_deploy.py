from fastapi.testclient import TestClient

from tdp_server.main import app

client = TestClient(app)


def test_deploy1():
    query_params1 = {
        "force_stale_update": False,
        "dry": False,
        "mock_deploy": True,
        "validate": True,
    }
    client.post("/api/v1/plan/dag")
    response = client.post("/api/v1/deploy", params=query_params1)
    assert response.status_code == 200
    assert response.json() == "Deployment finished with success."


def test_deploy2():
    query_params1 = {
        "force_stale_update": False,
        "dry": False,
        "mock_deploy": True,
        "validate": True,
    }
    response = client.post("/api/v1/deploy", params=query_params1)
    assert response.status_code == 500
    assert response.json() == {
        "detail": "No planned deployment found, please run `tdp plan` first."
    }


def test_deploy3():
    query_params2 = {
        "force_stale_update": False,
        "dry": True,
        "mock_deploy": False,
        "validate": True,
    }
    client.post("/api/v1/plan/dag")
    response = client.post("/api/v1/deploy", params=query_params2)
    assert response.status_code == 200
    assert response.json() == "Deployment successfuly executed in dry mode"


def test_deploy4():
    query_params3 = {
        "force_stale_update": False,
        "dry": False,
        "mock_deploy": True,
        "validate": False,
    }
    client.post("/api/v1/plan/dag")
    response = client.post("/api/v1/deploy", params=query_params3)
    assert response.status_code == 200
    assert response.json() == "Deployment finished with success."


def get_test_deploy():
    response = client.get("/api/v1/deploy")
    assert response.status_code == 500
    assert response.json() == {
        "detail": {"NoResultFound": "No row was found when one was required"}
    }
