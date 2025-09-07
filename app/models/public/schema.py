from pydantic import BaseModel, computed_field

from app.models.public.songs import SongPublic


class SongsParentModel(BaseModel):
    songs: list[SongPublic]

    @computed_field
    @property
    def songs_by_title(self) -> dict[str, SongPublic]:
        return {song.title: song for song in self.songs}

    def get_song_by_title(self, title: str) -> SongPublic | None:
        return self.songs_by_title.get(title)


class IncludeSpanishRequest(BaseModel):
    text: str
    values: list[str] | None = None


class IncludeSpanishResponse(BaseModel):
    text_data: str
    json_data: SongsParentModel