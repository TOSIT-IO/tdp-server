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

- Should the url for the endpoints start with `/api/v1` as it was the case in the first version and is the case in Ambari but SHOULD not be the case according to the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls) and just directly start from `/` ?

- Keep some verbs in the url such as `deploy`,`reconfigure` although the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls) state that it MUST be verb-free.

- Use Cursor-based pagination instead of offset-based as it SHOULD be used according to the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#pagination)?

- [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#http-status-codes-and-errors) state that error 422 must not be used. However, this status code is automatically added by the library fastapi_pagination which throws this error if it cannot proceed with the pagination and it does not seem to be configurable.

- Endpoints `deployments` which conists of get methods giving informations about past and current deployments and the endpoint `deploy` a post method which executes the planned deployment have been seperated into two different endpoints as they perform actions of different type. There wasn't that distinction in the first server.

- The previous `schema` endpoint has been attached to services as it concerns them and is therefore a subresource and is referenced via a path-segment as described in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls).

- Although `components` is a subresource of `service` it has been kept seperated to limit the number of resources in the latter endpoint [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls).

- The `status` endpoint has been added which corresponds to the `tdp browse show` command in tdp-lib. It is an independant endpoint as it concerns all services and all components and are therefore not passed in the url. However, `status-history` which gives the history of all updates of a specific component is a subresource of components and has therefore been added there.

- Instead of having three different endpoints in the group `operations` (all, dag, other), only one has been maintained with a query parameter as option to access each subresource.

- The `validate` endpoint which validates the variables has been added to have the same functionnality as in tdp-lib.

- The put methods `services/{service_id}/variables` and `services/{service_id}/components/{component_id}/variables` correspond to their old counterpart without the `variables` at the end since the use is to modify the service or component variables. The paths without the `/variables` now corrspond to a new functionality which is to modify the service or component version and be able to start or stop it.

- New functionalities have been added compared to the previous server such as:
    - `plan/import` to plan a deployment from an imported file.
    - `plan/custom` to customize a deployment plan.
    - `services/{service_id}/components/{component_id}/stales` pass the component to stale.
