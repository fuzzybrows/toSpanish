import enum
from enum import auto
from functools import cached_property

from pydantic import BaseModel, computed_field

class GeminiModels(str, enum.Enum):
    TWO_FLASH = "gemini-2.0-flash"
    TWO_FIVE_FLASH = "gemini-2.5-flash"
    TWO_FIVE_PRO = "gemini-2.5-pro"
    THREE_FLASH_PREVIEW = "gemini-3-flash-preview"
    THREE_PRO_PREVIEW = "gemini-3-pro-preview"



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


class SongsParentModel(BaseModel):
    songs: list[Song]

    @computed_field
    @property
    def songs_by_title(self) -> dict[str, Song]:
        return {song.title: song for song in self.songs}

    def get_song_by_title(self, title: str) -> Song | None:
        return self.songs_by_title.get(title)


class IncludeSpanishRequest(BaseModel):
    text: str
    values: list[str] | None = None

class IncludeSpanishResponse(BaseModel):
    text_data: str
    json_data: SongsParentModel