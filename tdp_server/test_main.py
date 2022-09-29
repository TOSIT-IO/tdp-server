def test_app_creates(app):  # noqa
    assert app


def test_app_working(app, client):  # noqa
    resp = client.get("/docs")
    assert resp.status_code == 200
