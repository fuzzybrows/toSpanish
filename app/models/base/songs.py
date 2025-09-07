import enum
from enum import auto
from pydantic import model_validator

from sqlmodel import SQLModel


class VerseType(str, enum.Enum):
    VERSE = auto()
    CHORUS = auto()
    BRIDGE = auto()
    INTRO = auto()
    OUTRO = auto()
    VAMP = auto()

class SongLanguage(str, enum.Enum):
    SPANISH = "SPANISH"
    ENGLISH = "ENGLISH"
    YORUBA = "YORUBA"
    IGBO = "IGBO"
    HAUSA = "HAUSA"
    PIDGIN_ENGLISH = "PIDGIN_ENGLISH"


class LineBase(SQLModel):
    english: str | None = None
    spanish: str | None = None
    yoruba: str | None = None
    igbo: str | None = None
    hausa: str | None = None
    pidgin_english: str | None = None

    @model_validator(mode="after")
    def validate_line(self):
        if not (self.english or self.spanish or self.yoruba or self.igbo or self.hausa or self.pidgin_english):
            raise ValueError("At least one line must be provided")
        return self


class VerseBase(SQLModel):
    type: VerseType


class SongBase(SQLModel):
    title: str
    language: SongLanguage