from schemas.users import UserResponse
from src.models.users import UserOrm
from src.repos.mappers.base import DataMapper


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = UserResponse
