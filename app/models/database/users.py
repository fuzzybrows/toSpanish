from uuid import UUID, uuid4

from sqlmodel import Field

from app.models.base.users import UserBase


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field()
