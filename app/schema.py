import enum
from enum import auto

from pydantic import BaseModel


class VerseType(str, enum.Enum):
    VERSE = auto()
    CHORUS = auto()
    BRIDGE = auto()
    INTRO = auto()
    OUTRO = auto()
    VAMP = auto()


class Line(BaseModel):
    english: str
    spanish: str | None = None


class Verse(BaseModel):
    lines: list[Line]
    type: VerseType


class Song(BaseModel):
    title: str
    verses: list[Verse]


class Response(BaseModel):
    songs: list[Song]


class IncludeSpanishRequest(BaseModel):
    text: str
    values: list[str] | None = None

class IncludeSpanishResponse(BaseModel):
    text_data: str
    json_data: Response