from fastapi import status

from tdp_server.core.config import settings


def test_get_component(client):
    resp = client.get(f"{settings.API_V1_STR}/service/mock/component/node")
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert response["id"] == "node"


def test_get_component_does_not_exist(client):
    resp = client.get(f"{settings.API_V1_STR}/service/mock/component/namenode")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_put_component_without_message(client):
    data = {
        "variables": {"key": "replaced with put", "a_test_put_key": "keylogs"},
    }
    resp = client.put(f"{settings.API_V1_STR}/service/mock/component/node", json=data)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    resp = client.get(f"{settings.API_V1_STR}/service/mock/component/node")
    response = resp.json()
    assert "a_test_put_key" not in response["variables"]


def test_put_component(client):
    data = {
        "message": "updating configuration with a put component",
        "variables": {"key": "replaced with put", "a_second_put_key": "key"},
    }
    resp = client.put(f"{settings.API_V1_STR}/service/mock/component/node", json=data)
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert data["message"] in response["message"]

    resp = client.get(f"{settings.API_V1_STR}/service/mock/component/node")
    response = resp.json()
    assert response["variables"] == data["variables"]


def test_patch_component_without_message(client):
    data = {
        "variables": {"key": "replaced with put", "a_test_put_key": "keylogs"},
    }
    resp = client.patch(f"{settings.API_V1_STR}/service/mock/component/node", json=data)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    resp = client.get(f"{settings.API_V1_STR}/service/mock/component/node")
    response = resp.json()
    assert "a_test_put_key" not in response["variables"]


def test_patch_component(client):
    data = {
        "message": "updating configuration with a patch component",
        "variables": {"another_key": "replaced with patch"},
    }
    resp = client.patch(f"{settings.API_V1_STR}/service/mock/component/node", json=data)
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert data["message"] in response["message"]

    resp = client.get(f"{settings.API_V1_STR}/service/mock/component/node")
    response = resp.json()
    assert response["variables"] != data["variables"]
    assert response["variables"].items() >= data["variables"].items()
