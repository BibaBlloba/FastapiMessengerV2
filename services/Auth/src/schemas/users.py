from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRequestCreate(BaseModel):
    """Схема для создания пользователя (запрос от клиента)"""

    login: str = Field(..., max_length=100)
    username: str = Field(..., max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: str


class UserCreate(BaseModel):
    """Схема для создания пользователя (внутренняя)"""

    login: str = Field(..., max_length=100)
    username: str = Field(..., max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False


class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя"""

    id: UUID
    login: str
    username: str
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """Схема для обновления пользователя (запрос от клиента)"""

    login: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
    is_verified: Optional[bool] = Field(None)


class UserUpdate(BaseModel):
    """Схема для обновления пользователя (внутренняя)"""

    login: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    hashed_password: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
    is_verified: Optional[bool] = Field(None)


class UserLogin(BaseModel):
    """Схема для входа пользователя"""

    login: str
    password: str


class Token(BaseModel):
    """Схема для токена"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема для данных в токене"""

    user_id: Optional[UUID] = None
    username: str = None
