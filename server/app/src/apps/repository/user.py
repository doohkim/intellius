from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...core.database.connection import get_db
from ..model.user import User


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user

    def get_user_by_username(self, username: str) -> User:
        return self.session.scalar(select(User).where(User.username == username))

    def get_user_by_id(self, user_id: str) -> User:
        return self.session.scalar(select(User).where(User.id == user_id))
