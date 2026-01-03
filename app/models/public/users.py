from uuid import UUID

from app.models.base.users import UserBase


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None


class UserPublic(UserBase):
    id: UUID
