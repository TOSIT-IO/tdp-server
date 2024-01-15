from fastapi.testclient import TestClient

from tdp_server.main import app

client = TestClient(app)


def test_show_plan():
    client.post("/api/v1/plan/dag")
    response = client.get("/api/v1/plan")
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag1():
    query_params1 = {
        "targets": None,
        "sources": None,
        "restart": False,
        "reverse": False,
        "stop": False,
        "preview": False,
    }
    response = client.post("/api/v1/plan/dag", params=query_params1)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag2():
    query_params2 = {
        "targets": None,
        "sources": None,
        "restart": True,
        "reverse": False,
        "stop": False,
        "preview": False,
    }
    response = client.post("/api/v1/plan/dag", params=query_params2)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag3():
    query_params3 = {
        "targets": None,
        "sources": None,
        "restart": False,
        "reverse": True,
        "stop": False,
        "preview": False,
    }
    response = client.post("/api/v1/plan/dag", params=query_params3)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag4():
    query_params4 = {
        "targets": None,
        "sources": None,
        "restart": False,
        "reverse": True,
        "stop": True,
        "preview": False,
    }
    response = client.post("/api/v1/plan/dag", params=query_params4)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag5():
    query_params5 = {
        "targets": None,
        "sources": None,
        "restart": False,
        "reverse": False,
        "stop": False,
        "preview": True,
    }
    response = client.post("/api/v1/plan/dag", params=query_params5)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag6():
    query_params5 = {
        "targets": None,
        "sources": None,
        "restart": False,
        "reverse": False,
        "stop": False,
        "preview": False,
        "rolling_restart": 5,
    }
    response = client.post("/api/v1/plan/dag", params=query_params5)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_plan_dag7():
    query_params1 = {
        "targets": None,
        "sources": None,
        "restart": True,
        "reverse": False,
        "stop": True,
        "preview": False,
    }
    response = client.post("/api/v1/plan/dag", params=query_params1)
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Cannot use `--restart` and `--stop` at the same time."
    }
