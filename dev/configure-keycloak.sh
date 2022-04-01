export PATH="$PATH:/opt/jboss/keycloak/bin"
export REALM="tdp_server_dev"
export SCOPE_NS="tdp_server"

login() {
    kcadm.sh config credentials --server http://${KC_ADDRESS:-localhost}:8080/auth --realm master --user "$KEYCLOAK_USER" --password "$KEYCLOAK_PASSWORD"
}

for i in {1..5}; do login && break || sleep 4; done

# Access token duration: 1H
kcadm.sh create realms --set "realm=$REALM" --set "enabled=true" --set "accessTokenLifespan=3600"

kcadm.sh create users --target-realm $REALM --set "username=test_user1" --set "enabled=true"
kcadm.sh set-password --target-realm $REALM --username test_user1 --new-password toto

createClientScope() {
kcadm.sh create client-scopes --target-realm $REALM -f - << EOF
{
    "name": "$SCOPE_NS:$1",
    "protocol": "openid-connect",
    "protocolMappers": [
        {
            "name": "audience-mapping",
            "protocol": "openid-connect",
            "protocolMapper": "oidc-audience-mapper",
            "config": {
                "included.client.audience": "tdp_server_id",
                "access.token.claim": true,
                "id.token.claim": true
            }
        }
    ]
}
EOF
}

createClientScope "read"
createClientScope "write"
createClientScope "execute"


kcadm.sh create clients --target-realm $REALM --set "enabled=true" --set "bearerOnly=true" --set "clientId=tdp_server_id" 
kcadm.sh create clients --target-realm $REALM -f - << EOF
{
    "clientId": "tdp_auth",
    "enabled": true,
    "publicClient": true,
    "directAccessGrantsEnabled": true,
    "redirectUris": ["http://localhost:8000/api/v1/*"],
    "optionalClientScopes": ["$SCOPE_NS:read", "$SCOPE_NS:write", "$SCOPE_NS:execute"],
    "webOrigins": ["*"]
}
EOF
