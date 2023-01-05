import secrets
from copy import copy
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from tdp_server.models import OAuth2Client
from tdp_server.schemas import CreateClient


class ClientService:
    @staticmethod
    def create_client(db: Session, request: CreateClient) -> OAuth2Client:
        client_id = secrets.token_hex(24)
        client_id_iat = datetime.utcnow().timestamp()

        client = OAuth2Client(client_id=client_id, client_id_issued_at=client_id_iat)
        client_metadata = request.dict()

        client.set_client_metadata(client_metadata)
        if request.token_endpoint_auth_method == "":
            client.client_secret = ""
        else:
            client.client_secret = secrets.token_hex(48)
        db.add(client)
        client = copy(client)
        db.commit()
        return client

    @staticmethod
    def get_client(db: Session, client_id: str) -> Optional[OAuth2Client]:
        return db.query(OAuth2Client).where(OAuth2Client.client_id == client_id).first()

    @staticmethod
    def get_clients(db: Session) -> List[OAuth2Client]:
        return db.query(OAuth2Client).all()
