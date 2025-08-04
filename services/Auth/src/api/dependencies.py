from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from database import async_session_maker
from src.schemas.users import TokenData, UserResponse
from src.services.auth import AuthService
from utils.db_manager import DbManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

auth_service = AuthService()


async def get_db():
    async with DbManager(session_factory=async_session_maker) as db:
        yield db


DbDep = Annotated[DbManager, Depends(get_db)]


async def get_current_user(
    db: DbDep, token: str = Depends(oauth2_scheme)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = auth_service.decode_token(token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.JWTError:
        raise credentials_exception

    user = await db.users.get_user_without_pwd(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


CurrentActiveUserDap = Annotated[UserResponse, Depends(get_current_active_user)]
