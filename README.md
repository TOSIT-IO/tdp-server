# TDP SERVER

## Run TDP Server

### Preparation

#### Start development environment
```bash
# Start docker services
docker compose -f dev/docker-compose.yml up -d
```

#### Install dependencies, configure, create tables
```bash
poetry install
poetry run githooks setup
cp dev/.env-dev .env # fill the 3 last variables with the right values
python tdp_server/initialize_database.py
```

### Start server

```bash
uvicorn tdp_server.main:app --reload
```

## Access documentation UIs

### OpenAPI UI

http://localhost:8000/docs

### ReDoc UI

http://localhost:8000/redoc

## Access REST API with cURL

```bash
token=$(python get_token.py)
curl -H "Authorization: Bearer $token" http://localhost:8000/api/v1/service/
```
