import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from ..model.user import User


class UserService:
    """사용자 관련 모든 기능"""

    def __init__(self):
        self.jwt_algorithm = "HS256"
        self.encoding = "UTF-8"
        self.secret_key = (
            "0600e9c10f96e2a483bf4343e312614f5a8315dcbac23908c4a1f33b4a715fda"
        )

    def hash_password(self, plain_password: str) -> str:
        """비밀번호 해시화"""
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return bcrypt.checkpw(
            plain_password.encode(self.encoding), hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        """JWT 토큰 생성"""
        return jwt.encode(
            {"sub": username, "exp": datetime.now() + timedelta(days=7)},
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str) -> str:
        """JWT 토큰 디코딩"""
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        return payload["sub"]

    def authenticate_user(
        self, username: str, password: str, user_repo
    ) -> Optional[User]:
        """사용자 인증"""
        user = user_repo.get_user_by_username(username)
        if not user:
            return None

        if self.verify_password(password, user.hashed_password):
            return user
        return None
