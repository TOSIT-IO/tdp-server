COMMON_RESPONSES = {
    401: {
        "description": "Unauthenticated",
        "content": {
            "application/json": {
                "example": {"detail": "Error during authentication validation (reason)"}
            }
        },
    },
    403: {
        "description": "Not enough privileges",
        "headers": {
            "WWW-Authenticate": {
                "schema": {"type": "string"},
                "description": "Authentication method to use",
            }
        },
        "content": {
            "application/json": {"example": {"detail": "Not enough permissions"}}
        },
    },
}

SERVICE_ID_DOES_NOT_EXIST_ERROR = {
    404: {
        "description": "Service id does not exist",
        "content": {
            "application/json": {"example": {"detail": "{service_id} does not exist"}}
        },
    }
}

COMPONENT_ID_DOES_NOT_EXIST_ERROR = {
    404: {
        "description": "Component id does not exist",
        "content": {
            "application/json": {"example": {"detail": "{component_id} does not exist"}}
        },
    }
}

COMMON_DEPLOYMENT_ARGS = {
    409: {
        "description": "Another deployment is still running, only one deployment at a time is allowed",
        "content": {
            "application/json": {
                "example": {"detail": "another deployment is still running"}
            }
        },
    }
}

IMPORT_FILE_DOES_NOT_EXIST = {
    400: {
        "description": "File does not exist",
        "content": {"application/json": {"example": {"detail": "File does not exist"}}},
    }
}
