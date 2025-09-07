import pytest
from pydantic import ValidationError

from app.models.public.songs import LinePublic, VersePublic, SongPublic
from app.models.base.songs import VerseType, SongLanguage


def test_line_model_valid(sample_line):
    """Test that a valid line model can be created."""
    assert sample_line.english == "This is a test line"
    assert sample_line.spanish == "Esta es una línea de prueba"


def test_line_model_validation():
    """Test that line model validation works correctly."""
    # Test that at least one language field must be provided
    with pytest.raises(ValidationError):
        LinePublic()


def test_verse_model_valid(sample_verse):
    """Test that a valid verse model can be created."""
    assert sample_verse.type == VerseType.VERSE
    assert len(sample_verse.lines) == 2
    assert sample_verse.lines[0].english == "Line 1"
    assert sample_verse.lines[0].spanish == "Línea 1"


def test_song_model_valid(sample_song):
    """Test that a valid song model can be created."""
    assert sample_song.title == "Test Song"
    assert sample_song.language == SongLanguage.ENGLISH
    assert len(sample_song.verses) == 2
    
    # Check verse types
    assert sample_song.verses[0].type == VerseType.VERSE
    assert sample_song.verses[1].type == VerseType.CHORUS
    
    # Check lines in first verse
    assert len(sample_song.verses[0].lines) == 2
    assert sample_song.verses[0].lines[0].english == "Verse line 1"
    assert sample_song.verses[0].lines[0].spanish == "Verso línea 1"


def test_song_model_validation():
    """Test that song model validation works correctly."""
    # Test that title is required
    with pytest.raises(ValidationError):
        SongPublic(language=SongLanguage.ENGLISH, verses=[])
    
    # Test that language is required
    with pytest.raises(ValidationError):
        SongPublic(title="Test Song", verses=[])