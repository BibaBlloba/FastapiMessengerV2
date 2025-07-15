from sqlalchemy.sql import select

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
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]
