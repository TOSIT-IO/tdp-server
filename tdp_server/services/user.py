from sqlalchemy import select
from sqlalchemy.orm.session import Session

from tdp_server.models import User


class UserDoesNotExist(Exception):
    pass


class UserService:
    @staticmethod
    def oauth2_callback(db: Session, token: dict) -> User:
        try:
            user = UserService.get_by_oauth2_account(db, token["userinfo"]["sub"])
        except UserDoesNotExist:
            user = UserService.register_oauth2_user(db, token)

        return user

    @staticmethod
    def get_by_oauth2_account(db: Session, id: str) -> User:
        user = db.execute(
            select(User).where(User.account_id == id)
        ).scalar_one_or_none()
        if user is None:
            raise UserDoesNotExist()
        return user

    @staticmethod
    def register_oauth2_user(db: Session, token: dict) -> User:
        user = User(
            access_token=token["access_token"],
            expires_at=token["expires_at"],
            refresh_token=token["refresh_token"],
            account_id=token["userinfo"]["sub"],
            account_email=token["userinfo"]["email"],
        )
        db.add(user)
        db.commit()
        return user
