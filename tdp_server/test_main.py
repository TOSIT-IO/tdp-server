from fastapi.testclient import TestClient

from tdp_server.main import app

client = TestClient(app)


def test_get_all_get_endpoints():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [
        {"path": "/api/v1/deploy", "method": "get_deployment_status"},
        {"path": "/docs", "method": "swagger_ui_html"},
        {"path": "/api/v1/operations", "method": "get_operations"},
        {"path": "/docs/oauth2-redirect", "method": "swagger_ui_redirect"},
        {"path": "/api/v1/deployments/{deployement_id}", "method": "get_deployment"},
        {"path": "/api/v1/plan", "method": "show_plan"},
        {"path": "/api/v1/configuration/validate", "method": "get_validate"},
        {"path": "/", "method": "read_get_endpoints"},
        {"path": "/redoc", "method": "redoc_html"},
        {
            "path": "/api/v1/configuration/services/{service_id}",
            "method": "get_service",
        },
        {
            "path": "/api/v1/deployments/{deployement_id}/operations/{operation_order}",
            "method": "get_deployment_operation",
        },
        {
            "path": "/api/v1/configuration/services/{service_id}/components/{component_id}/variables",
            "method": "get_component_variables",
        },
        {
            "path": "/api/v1/configuration/services/{service_id}/variables",
            "method": "get_service_variables",
        },
        {"path": "/api/v1/configuration/history", "method": "get_history"},
        {
            "path": "/api/v1/configuration/services/{service_id}/components/{component_id}/history",
            "method": "get_component_history",
        },
        {"path": "/api/v1/configuration", "method": "get_status"},
        {"path": "/api/v1/deployments", "method": "get_deployments"},
        {
            "path": "/api/v1/configuration/services/{service_id}/components/{component_id}",
            "method": "get_component",
        },
        {
            "path": "/api/v1/configuration/services/{service_id}/components",
            "method": "get_components",
        },
        {
            "path": "/api/v1/configuration/services/{service_id}/schema",
            "method": "get_service_schema",
        },
        {
            "path": "/api/v1/configuration/services{service_id}/history",
            "method": "get_service_history",
        },
        {"path": "/openapi.json", "method": "openapi"},
        {"path": "/api/v1/configuration/services", "method": "get_services"},
    ]


def test_endpoints_response_type():
    for path in app.routes:
        response = client.get(f"{path}")
        # assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)
