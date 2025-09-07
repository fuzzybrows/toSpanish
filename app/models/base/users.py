from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
