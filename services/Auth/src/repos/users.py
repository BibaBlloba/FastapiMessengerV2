from sqlalchemy.sql import select

from schemas.users import UserCreate
from src.models.users import UserOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import UserDataMapper


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hashedPwd(
        self,
        username: str | None = None,
        login: str | None = None,
    ):
        if id:
            query = select(self.model).filter_by(username=username)
        else:
            query = select(self.model).filter_by(login=login)

        result = await self.session.execute(query)
        user = result.scalars().first()  # Get first result or None

        if not user:
            return None

        return UserCreate(
            login=user.login,
            username=user.username,
            email=user.email,
            phone=user.phone,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )
