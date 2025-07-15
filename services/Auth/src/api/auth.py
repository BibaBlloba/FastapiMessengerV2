from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import CurrentActiveUserDap, DbDep
from services.auth import AuthService
from src.schemas.users import (Token, UserCreate, UserRequestCreate,
                               UserResponse)

router = APIRouter(prefix='', tags=['Auth'])


auth_service = AuthService()


# TODO: Протестить
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = auth_service.create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserResponse)
async def read_users_me(current_user: CurrentActiveUserDap):
    return current_user


@router.post('/register')
async def register_user(
    db: DbDep,
    data: UserRequestCreate = Body(),
):
    _data_without_passwd = data.model_dump()
    _data_without_passwd.pop('password')
    hashed_password = AuthService().hash_password(data.password)
    hashed_user_data = UserCreate(
        hashed_password=hashed_password,
        **_data_without_passwd,
    )

    result = await db.users.add(hashed_user_data)

    await db.commit()
    return result
