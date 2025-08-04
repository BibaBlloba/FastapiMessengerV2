from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext

from database import async_session_maker
from src.config import settings
from src.schemas.users import UserResponse
from src.services.base import BaseService
from utils.db_manager import DbManager


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXIPRE_MINUTES
        )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError('Token has expired')
        except jwt.JWTError as e:
            raise jwt.JWTError(f'Could not validate credentials: {str(e)}')

    async def get_user(self, username: str) -> Optional[UserResponse]:
        async with DbManager(session_factory=async_session_maker) as db:
            user: UserResponse = await db.users.get_user_without_pwd(username)
            return user

    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[UserResponse]:
        """Возвращает схему пользователя по username и password"""

        user = await self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
