#!/usr/bin/env python3

import httpx

# curl "http://localhost:8080/auth/realms/tdp_server/protocol/openid-connect/token" -d "client_id=tdp_server&grant_type=password&username=user&password=secret&scope=openid tdp_server:read tdp_server:write tdp_server:execute"

scopes = ["openid", "tdp_server:read", "tdp_server:write", "tdp_server:execute"]

data = {
    "client_id": "tdp_server",
    "grant_type": "password",
    "username": "user",
    "password": "secret",
    "scope": " ".join(scopes),
}
response = httpx.post(
    "http://localhost:8080/auth/realms/tdp_server/protocol/openid-connect/token",
    data=data,
)

response.raise_for_status()
response_data = response.json()

print(response_data["access_token"])
