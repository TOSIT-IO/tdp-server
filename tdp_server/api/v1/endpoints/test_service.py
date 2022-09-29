from fastapi import status

from tdp_server.core.config import settings


def test_get_services(client):
    resp = client.get(f"{settings.API_V1_STR}/service/")
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert len(response) > 0
    assert response[0]["id"] == "mock"


def test_get_service(client):
    resp = client.get(f"{settings.API_V1_STR}/service/mock")
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert response["id"] == "mock"


def test_get_service_does_not_exist(client):
    resp = client.get(f"{settings.API_V1_STR}/service/no_mock")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_put_service_without_message(client):
    data = {
        "variables": {"key": "replaced with put", "a_test_put_key": "keylogs"},
    }
    resp = client.put(f"{settings.API_V1_STR}/service/mock", json=data)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    resp = client.get(f"{settings.API_V1_STR}/service/mock")
    response = resp.json()
    assert "a_test_put_key" not in response["variables"]


def test_put_service(client):
    data = {
        "message": "updating configuration with a put",
        "variables": {"key": "replaced with put", "a_second_put_key": "key"},
    }
    resp = client.put(f"{settings.API_V1_STR}/service/mock", json=data)
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert data["message"] in response["message"]

    resp = client.get(f"{settings.API_V1_STR}/service/mock")
    response = resp.json()
    assert response["variables"] == data["variables"]


def test_patch_service_without_message(client):
    data = {
        "variables": {"key": "replaced with patch", "a_test_put_key": "keylogs"},
    }
    resp = client.patch(f"{settings.API_V1_STR}/service/mock", json=data)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    resp = client.get(f"{settings.API_V1_STR}/service/mock")
    response = resp.json()
    assert "a_test_put_key" not in response["variables"]


def test_patch_service(client):
    data = {
        "message": "updating configuration with a patch",
        "variables": {"another_key": "replaced with patch"},
    }
    resp = client.patch(f"{settings.API_V1_STR}/service/mock", json=data)
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    assert data["message"] in response["message"]

    resp = client.get(f"{settings.API_V1_STR}/service/mock")
    response = resp.json()
    assert response["variables"] != data["variables"]
    assert response["variables"].items() >= data["variables"].items()
