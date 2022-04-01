#!/usr/bin/env python3

import requests

# curl "http://localhost:8080/auth/realms/tdp_server_dev/protocol/openid-connect/token" -d "client_id=tdp_auth" -d "grant_type=password" -d "username=test_user1" -d "password=toto" -d "scope=openid tdp_server:read tdp_server:write tdp_server:execute"

scopes = ["openid", "tdp_server:read", "tdp_server:write", "tdp_server:execute"]

data = {
    "client_id": "tdp_auth",
    "grant_type": "password",
    "username": "test_user1",
    "password": "toto",
    "scope": " ".join(scopes),
}
response = requests.post(
    "http://localhost:8080/auth/realms/tdp_server_dev/protocol/openid-connect/token",
    data=data,
)

response.raise_for_status()
response_data = response.json()

print(response_data["access_token"])
