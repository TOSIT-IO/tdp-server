from fastapi.testclient import TestClient

from tdp_server.main import app
from tdp_server.schemas.deployments import DeploymentLog

client = TestClient(app)


def test_deployments1():
    client.post("/api/v1/plan/dag")
    response = client.get("/api/v1/deployments/{deployement_id}?deployment_id=1")
    assert response.status_code == 200
