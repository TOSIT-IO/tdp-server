from pathlib import Path
from typing import Dict, Tuple

import pytest
import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tdp.core.collection import Collection
from tdp.core.collections import Collections
from tdp.core.dag import Dag
from tdp.core.variables import ClusterVariables

from tdp_server.api.dependencies import get_cluster_variables, get_dag
from tdp_server.api.openid_dependencies import mock_validate_token, validate_token
from tdp_server.core.config import settings
from tdp_server.db.base import Base
from tdp_server.main import create_app

MOCK_SERVICE_DAG = [
    {"name": "mock_node_install", "depends_on": []},
    {"name": "mock_node_config", "depends_on": ["mock_node_install"]},
    {"name": "mock_node_start", "depends_on": ["mock_node_config"]},
    {"name": "mock_node_init", "depends_on": ["mock_node_start"]},
    {"name": "mock_install", "noop": True, "depends_on": ["mock_node_install"]},
    {
        "name": "mock_config",
        "noop": True,
        "depends_on": ["mock_install", "mock_node_config"],
    },
    {
        "name": "mock_start",
        "noop": True,
        "depends_on": ["mock_config", "mock_node_start"],
    },
    {"name": "mock_init", "noop": True, "depends_on": ["mock_start", "mock_node_init"]},
]


@pytest.fixture(scope="session")
def minimal_collection(tmp_path_factory: pytest.TempPathFactory) -> Path:
    collection = tmp_path_factory.mktemp("minimal_collection")

    tdp_lib_dag = collection / "tdp_lib_dag"
    playbooks = collection / "playbooks"
    tdp_vars_defaults = collection / "tdp_vars_defaults"
    mock_defaults = tdp_vars_defaults / "mock"

    tdp_lib_dag.mkdir()
    playbooks.mkdir()
    tdp_vars_defaults.mkdir()
    mock_defaults.mkdir()

    with (tdp_lib_dag / "mock.yml").open("w") as fd:
        fd.write(yaml.dump(MOCK_SERVICE_DAG))

    with (mock_defaults / "mock.yml").open("w") as fd:
        fd.write(yaml.dump({"key": "value", "another_key": "another_value"}))

    return collection


@pytest.fixture(scope="module")
def mock_runtime(
    tmp_path_factory: pytest.TempPathFactory, minimal_collection: Path
) -> Tuple[Dag, ClusterVariables]:
    runtime = tmp_path_factory.mktemp("runtime")

    tdp_vars = runtime / "tdp_vars"

    tdp_vars.mkdir()

    settings.TDP_VARS = tdp_vars
    settings.TDP_COLLECTION_PATH = str(minimal_collection.absolute())
    settings.TDP_COLLECTIONS = Collections.from_collection_list(
        [Collection.from_path(settings.TDP_COLLECTION_PATH)]
    )

    dag = Dag(settings.TDP_COLLECTIONS)
    cluster_variables = ClusterVariables.initialize_cluster_variables(
        settings.TDP_COLLECTIONS, settings.TDP_VARS
    )

    return dag, cluster_variables


@pytest.fixture
def app(mock_runtime):
    app = create_app()

    dag, cluster_variables = mock_runtime

    # Disable token validation for tests
    app.dependency_overrides[validate_token] = mock_validate_token

    app.dependency_overrides[get_dag] = lambda: dag
    app.dependency_overrides[get_cluster_variables] = lambda: cluster_variables
    return app


@pytest.fixture
def client(app):
    client = TestClient(app)
    return client


@pytest.fixture
def session(app):
    engine = create_engine(settings.DATABASE_DSN, pool_pre_ping=True, future=True)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as session:
        Base.metadata.drop_all(session)
        Base.metadata.create_all(session)
        yield session
        Base.metadata.drop_all(session)
        session.commit()
