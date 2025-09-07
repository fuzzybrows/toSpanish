from app.models.base.songs import LineBase, VerseBase, SongBase


class LinePublic(LineBase):
    pass


class VersePublic(VerseBase):
    lines: list[LinePublic]


class SongPublic(SongBase):
    verses: list[VersePublic]