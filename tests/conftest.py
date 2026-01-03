import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.server import app
from app.models.public.schema import SongsParentModel
from app.models.public.songs import SongPublic, VersePublic, LinePublic
from app.models.base.songs import VerseType, SongLanguage


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def sample_line():
    """
    Create a sample line for testing.
    """
    return LinePublic(
        english="This is a test line",
        spanish="Esta es una línea de prueba"
    )


@pytest.fixture
def sample_verse():
    """
    Create a sample verse for testing.
    """
    return VersePublic(
        type=VerseType.VERSE,
        lines=[
            LinePublic(english="Line 1", spanish="Línea 1"),
            LinePublic(english="Line 2", spanish="Línea 2")
        ]
    )


@pytest.fixture
def sample_song():
    """
    Create a sample song for testing.
    """
    return SongPublic(
        title="Test Song",
        language=SongLanguage.ENGLISH,
        verses=[
            VersePublic(
                type=VerseType.VERSE,
                lines=[
                    LinePublic(english="Verse line 1", spanish="Verso línea 1"),
                    LinePublic(english="Verse line 2", spanish="Verso línea 2")
                ]
            ),
            VersePublic(
                type=VerseType.CHORUS,
                lines=[
                    LinePublic(english="Chorus line 1", spanish="Coro línea 1"),
                    LinePublic(english="Chorus line 2", spanish="Coro línea 2")
                ]
            )
        ]
    )


@pytest.fixture
def sample_songs_parent():
    """
    Create a sample songs parent model for testing.
    """
    return SongsParentModel(
        songs=[
            SongPublic(
                title="Test Song 1",
                language=SongLanguage.ENGLISH,
                verses=[
                    VersePublic(
                        type=VerseType.VERSE,
                        lines=[
                            LinePublic(english="Verse line 1", spanish="Verso línea 1"),
                            LinePublic(english="Verse line 2", spanish="Verso línea 2")
                        ]
                    )
                ]
            ),
            SongPublic(
                title="Test Song 2",
                language=SongLanguage.ENGLISH,
                verses=[
                    VersePublic(
                        type=VerseType.CHORUS,
                        lines=[
                            LinePublic(english="Chorus line 1", spanish="Coro línea 1"),
                            LinePublic(english="Chorus line 2", spanish="Coro línea 2")
                        ]
                    )
                ]
            )
        ]
    )