import pytest
from pydantic import ValidationError

from app.models.public.schema import SongsParentModel, IncludeSpanishRequest, IncludeSpanishResponse


def test_songs_parent_model_valid(sample_songs_parent):
    """Test that a valid songs parent model can be created."""
    assert len(sample_songs_parent.songs) == 2
    assert sample_songs_parent.songs[0].title == "Test Song 1"
    assert sample_songs_parent.songs[1].title == "Test Song 2"


def test_songs_parent_model_computed_field(sample_songs_parent):
    """Test that the computed field songs_by_title works correctly."""
    songs_by_title = sample_songs_parent.songs_by_title
    assert len(songs_by_title) == 2
    assert "Test Song 1" in songs_by_title
    assert "Test Song 2" in songs_by_title
    assert songs_by_title["Test Song 1"].title == "Test Song 1"
    assert songs_by_title["Test Song 2"].title == "Test Song 2"


def test_get_song_by_title(sample_songs_parent):
    """Test that get_song_by_title method works correctly."""
    song = sample_songs_parent.get_song_by_title("Test Song 1")
    assert song is not None
    assert song.title == "Test Song 1"
    
    # Test with non-existent title
    song = sample_songs_parent.get_song_by_title("Non-existent Song")
    assert song is None


def test_include_spanish_request_valid():
    """Test that a valid include Spanish request can be created."""
    request = IncludeSpanishRequest(text="Test text")
    assert request.text == "Test text"
    assert request.values is None
    
    request_with_values = IncludeSpanishRequest(text="Test text", values=["value1", "value2"])
    assert request_with_values.text == "Test text"
    assert request_with_values.values == ["value1", "value2"]


def test_include_spanish_request_validation():
    """Test that include Spanish request validation works correctly."""
    # Test that text is required
    with pytest.raises(ValidationError):
        IncludeSpanishRequest()


def test_include_spanish_response_valid(sample_songs_parent):
    """Test that a valid include Spanish response can be created."""
    response = IncludeSpanishResponse(
        text_data="Test text data",
        json_data=sample_songs_parent
    )
    assert response.text_data == "Test text data"
    assert response.json_data == sample_songs_parent
    assert len(response.json_data.songs) == 2


def test_include_spanish_response_validation():
    """Test that include Spanish response validation works correctly."""
    # Test that text_data is required
    with pytest.raises(ValidationError):
        IncludeSpanishResponse(json_data=SongsParentModel(songs=[]))
    
    # Test that json_data is required
    with pytest.raises(ValidationError):
        IncludeSpanishResponse(text_data="Test text data")