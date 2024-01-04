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

    [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls) recommends directly starting it from `/`, however the [Ambari server](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/components.md) choses this endpoint prefix and it explicits what the user is using. Moreover the [Naming Conventions of the Australian government API](https://api.gov.au/sections/naming-conventions.html) states that the version must be specified.

- For versioning `v1` has been chosen for first version.

    `v1` has been chosen like in the Ambari server, the [Naming Conventions of the Australian government API](https://api.gov.au/sections/naming-conventions.html) give an example with the version `v1`, however, the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#116) state that we must chose semantic versioning.

- All resources are pluralized except `plan`.

    Since all resources consist of several items (configurations, services, components, deployments), the resource name is in plural form as stated as a must requirement in the [Zalando API guideline](https://opensource.zalando.com/restful-api-guidelines/#134) and in the [Naming Conventions of the Australian government API](https://api.gov.au/sections/naming-conventions.html). Only the `\plan` resource is singular since there is only one plan before it can be deployed and also to be consistent with TDP lib.

- All resource names are written in lower-case.

    As stated in the [Naming Conventions of the Australian government API](https://api.gov.au/sections/naming-conventions.html) all resource names must be written in lower-case.

- Query parmeters in URL are written using snake_case.

    The [Naming Conventions of the Australian government API](https://api.gov.au/sections/naming-conventions.html) recommend using snake_case or camelcase for query parameters, however in the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/query-params/) snake_case is used and it is also the way to declare variables in python. Query parameters whch are used as path parameters in the URL are therefore also in snake_case although they shouldn't be according to the first document but is performed in the FastAPI documentation.

- Kebab-case will be used for path segments except query parameters.

    For now, no resource name or action is a combination of two words. However, if it is the case, kebab-case must be used as stated in the [Naming Conventions of the Australian government API](https://api.gov.au/sections/naming-conventions.html) and the [Zalando API guideline](https://opensource.zalando.com/restful-api-guidelines/#129).

- Verbs have been chosen where actions are done.

    The [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls) state that it MUST be verb-free and the same is mentioned in the[dreamfactory blog](https://blog.dreamfactory.com/best-practices-for-naming-rest-api-endpoints/). The reason is that with the path we should access ressources and the actions are defined with the GET, PUT, POST, PATCH, DELETE methods. However, we are not using a REST API and with `/plan` we perform different actions such as `resume` or `reconfigure` with the same post method and both actions are not performed on different resources so introducing a verb is the best way of description. For the `deploy` endpoint the question is more debatable, however the clearest wording is favored and therefore we chose to maintain the verb.

- No empty path segments and trailing slashes.

    The [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#136) state that the URL must not have any empty path segments or trailing slashes. The [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/query-params/) give an example where there is a trailing slash, however to be as clean as possible and avoid any confusion no trailing slash occurs in any URL.

- Used domain specific resource names.

    Each resource name is domain specific which represent either the elements in TDP (`/services` and `/components`) or actions in TDP Manager as stated as a must requirement in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#142).

- Resources and sub-resources are identified via path segments.

    The `components` resource is a sub-resource of `services` which is a sub-resource of `configurations`. The path segment for a component looks the following `/api/v1/configurations/services/{service_id}/components/{component_id}`. This has been chosen to improve consumer experience while following the setup of TDP. The [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#143) state this practice as a must requirement.

- Cursor-based pagination instead of offset-based has been chosen.

    This is stated as a SHOULD requirement in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#pagination).

- JSON is used as response body.

    The JSON format is used as response body of every endpoint so that each function returns a JSON object as stated as a must requirement in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#167). Schemas are written using the Pydantic BaseModel which will read the body as JSON. The [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/body/) shows this method to declare request bodies.

- Enum values are declared as UPPER_CASE.

    As recommended by the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#240) enum values should be written as UPPER_SNAKE_CASE.

### Endpoint specific

- Two different endpoint `deployment` and `deploy` for different actions.

    Endpoints `deployments` which consists of get methods giving informations about past and current deployments and the endpoint `deploy` a post method which executes the planned deployment have been seperated into two different endpoints as they perform actions of different type. There wasn't that distinction in the first server.

- `schema` resource has been attached to the `services` endpoint.

    The previous `schema` endpoint has been attached to services as it concerns them and is therefore a subresource and is referenced via a path-segment as described in the [Zalando API guidelines](https://opensource.zalando.com/restful-api-guidelines/#urls).

- Query parameters have been placed in endpoint `operations` to access the subresources.

    Instead of accessing the three different resources (all, dag, other) seperately in the endpoint `operations`,  only the root of the endpoint is being accessed at first and a query parameter enables the user to access the subresources.

- Addition of the endpoint `validate`.

    The `validate` endpoint which validates the variables has been added to have the same functionnality as in tdp-lib.

- Refactored the put methods of the endpoints `/configurations/services/{service_id}/` and `/configurations/services/{service_id}/components/{component_id}`.

    The put methods `/configurations/services/{service_id}/variables` and `/configurations/services/{service_id}/components/{component_id}/variables` correspond to their old counterpart without the `variables` at the end since the use is to modify the service or component variables. The paths without the `/variables` now corrspond to a new functionality which is to modify the service or component version and be able to start or stop it.

- New functionalities have been added to the `plan` endpoint compared to the previous server such as:
    - `/plan/import` to plan a deployment from an imported file.
    - `/plan/custom` to customize a deployment plan.

    These functionalities exist in TDP lib, so they can also be used in the server.
