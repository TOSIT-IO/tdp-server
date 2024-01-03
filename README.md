# TDP Server

`tdp-server` provides a server to interact with [`tdp-lib`](https://github.com/tOSIT-IO/tdp-lib).

## Requirements

The server is made with Python. The following is required:

- [Python](https://www.python.org/) `3.9.5`
- [Poetry](https://python-poetry.org/) `1.7.1`

## Installation

Install the `tdp-server` dependencies in the pyproject.toml as follows:

```bash
poetry install
```

## Usage

To see the specification:

```sh
# Launch the server
poetry run uvicorn tdp_server.main:app --reload
``` 

Specification is available at <http://localhost:8000/docs>.

## Discussion

### General

- Endpoint prefix `/api/v1` as base path has been chosen.

    [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls) recommends directly starting it from `/`, however the [Ambari server](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/components.md) choses this endpoint prefix and it explicits what the user is using.

- Verbs have been chosen where actions are done.

    The [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls) state that it MUST be verb-free and the same is mentioned in the[dreamfactory blog](https://blog.dreamfactory.com/best-practices-for-naming-rest-api-endpoints/). The reason is that with the path we should access ressources and the actions are defined with the GET, PUT, POST, PATCH, DELETE methods. However, with `/plan` we perform different actions such as `resume` or `reconfigure` with the same post method and both actions are not performed on different resources so introducing a verb is the best way of description. For the `deploy` endpoint the question is more debatable, however the clearest wording is favored and therefore we chose to maintain the verb.

- Cursor-based pagination instead of offset-based has been chosen.

    This is stated as a SHOULD requirement in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#pagination).

### Endpoint specific

- Two different endpoint `deployment` and `deploy` for different actions.

    Endpoints `deployments` which consists of get methods giving informations about past and current deployments and the endpoint `deploy` a post method which executes the planned deployment have been seperated into two different endpoints as they perform actions of different type. There wasn't that distinction in the first server.

- `schema` resource has been attached to the `services` endpoint.

    The previous `schema` endpoint has been attached to services as it concerns them and is therefore a subresource and is referenced via a path-segment as described in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls).

- Seperation of endpoints `components` and `services`.

    Although `components` is a subresource of `service` it has been kept seperated to limit the number of resources in the latter endpoint [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls).

- Addition of the endpoint `status`.

    The `status` endpoint has been added which corresponds to the `tdp status show` command in tdp-lib. It is an independant endpoint as it concerns all services and all components and are therefore not passed in the url. However, `status-history` which gives the history of all updates of a specific component is a subresource of components and has therefore been added there.

- Query parameters have been placed in endpoint `operations` to access the subresources.

    Instead of accessing the three different resources (all, dag, other) seperately in the endpoint `operations`,  only the root of the endpoint is being accessed at first and a query parameter enables the user to access the subresources.

- Addition of the endpoint `validate`.

    The `validate` endpoint which validates the variables has been added to have the same functionnality as in tdp-lib.

- Refactored the put methods of the endpoints `services/{service_id}/` and `services/{service_id}/components/{component_id}`.

    The put methods `services/{service_id}/variables` and `services/{service_id}/components/{component_id}/variables` correspond to their old counterpart without the `variables` at the end since the use is to modify the service or component variables. The paths without the `/variables` now corrspond to a new functionality which is to modify the service or component version and be able to start or stop it.

- New functionalities have been added to the `plan` endpoint compared to the previous server such as:
    - `plan/import` to plan a deployment from an imported file.
    - `plan/custom` to customize a deployment plan.

    These functionalities exist in TDP lib, so they can also be used in the server.
