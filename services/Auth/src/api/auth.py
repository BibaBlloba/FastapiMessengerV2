from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import CurrentActiveUserDap
from services.auth import AuthService
from src.schemas.users import Token, UserResponse

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


@router.get('/users/me/', response_model=UserResponse)
async def read_users_me(current_user: CurrentActiveUserDap):
    return current_user
