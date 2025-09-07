from typing import List

from sqlalchemy import Column, Enum as SQLAlchemyEnum
from sqlmodel import Relationship, Field, SQLModel

from app.models.base.songs import SongBase, VerseBase, LineBase, SongLanguage


class Song(SongBase, table=True):
    id: int = Field(..., index=True, primary_key=True)
    verses: List["Verse"] = Relationship(back_populates="song")


class Verse(VerseBase, table=True):
    id: int = Field(..., index=True, primary_key=True)
    lines: list["Line"] = Relationship(back_populates="verse")
    song_id: int | None = Field(None, foreign_key="song.id")
    song: Song | None = Relationship(back_populates="verses")


class Line(LineBase, table=True):
    id: int = Field(..., index=True, primary_key=True)
    verse_id: int | None = Field(None, foreign_key="verse.id")
    verse: Verse | None = Relationship(back_populates="lines")
