import os
import pytest
from unittest.mock import patch, MagicMock

from app.service import (
    retrieve_unprocessed_files,
    process_files,
    get_gemini_response,
    generate_with_spanish_translations,
    create_import_file,
    create_import_file_string, LYRICS_PROMPT
)
from app.models.base.songs import VerseType
from app.models.public.schema import SongsParentModel


@patch("os.listdir")
@patch("os.path.isdir")
@patch("builtins.open")
def test_retrieve_unprocessed_files(mock_open, mock_isdir, mock_listdir):
    """Test retrieving unprocessed files."""
    # Mock os.listdir to return a list of files
    mock_listdir.return_value = ["file1.txt", "file2.txt"]
    
    # Mock os.path.isdir to return False for all files
    mock_isdir.return_value = False
    
    # Mock open to return a file-like object
    mock_file = MagicMock()
    mock_file.__enter__.return_value.readlines.return_value = ["line1", "line2"]
    mock_open.return_value = mock_file
    
    # Call the function
    result = retrieve_unprocessed_files()
    
    # Check the result
    assert len(result) == 2
    assert result[0] == ["line1", "line2"]
    assert result[1] == ["line1", "line2"]


@patch("app.service.get_gemini_response")
def test_process_files_with_existing_songs(mock_get_gemini_response, sample_songs_parent, sample_song):
    """Test processing files when some songs already exist in the database."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.parsed = [sample_song]
    mock_get_gemini_response.return_value = mock_response
    
    # Create a mock songs database
    songs_db = SongsParentModel(songs=[])
    
    # Create raw files with one existing song and one new song
    raw_files = {
        "Test Song 1.txt": "Test song 1 content",
        "New Song.txt": "New song content"
    }
    
    # Mock the get_song_by_title method
    # songs_db.get_song_by_title = MagicMock()
    # songs_db.get_song_by_title.side_effect = lambda title: sample_song if title == "Test Song 1" else None
    with patch('app.service.SongsParentModel.get_song_by_title') as mock_get_song_by_title:
        mock_get_song_by_title.side_effect = [sample_song, None]

        # Call the function
        result = process_files(raw_files=raw_files, songs_db=songs_db, write_to_file=False)

    # Check the result
    assert len(result.songs) == 2  # One existing song and one new song

    # Verify the mock was called with the new song only
    mock_get_gemini_response.assert_called_once()


@patch("app.service.GENAI_CLIENT.models.generate_content")
def test_get_gemini_response(mock_generate_content):
    """Test getting a response from the Gemini AI model."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.parsed = [{"title": "Test Song"}]
    mock_generate_content.return_value = mock_response
    
    # Call the function
    result = get_gemini_response(prompt="Test prompt", values=["Test value"])
    
    # Check the result
    assert result == mock_response
    
    # Verify the mock was called with the correct arguments
    mock_generate_content.assert_called_once()


@patch("app.service.get_gemini_response")
def test_generate_with_spanish_translations(mock_get_gemini_response, sample_song):
    """Test generating Spanish translations."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.parsed = [sample_song]
    mock_get_gemini_response.return_value = mock_response
    
    # Call the function
    result = generate_with_spanish_translations(texts=["Test text"])
    
    # Check the result
    assert len(result.songs) == 1
    assert result.songs[0] == sample_song
    
    # Verify the mock was called with the correct arguments
    mock_get_gemini_response.assert_called_once_with(prompt=LYRICS_PROMPT, values=["Test text"])


@patch("builtins.open")
def test_create_import_file(mock_open, sample_songs_parent):
    """Test creating an import file."""
    # Mock open to return a file-like object
    mock_file = MagicMock()
    mock_open.return_value = mock_file
    
    # Call the function
    create_import_file(structured_raw_file=sample_songs_parent, importable_file_path="test_path")
    
    # Verify the mock was called with the correct arguments
    mock_open.assert_called_once_with("test_path", "w")
    mock_file.__enter__.return_value.write.assert_called_once()


def test_create_import_file_string(sample_songs_parent):
    """Test creating an import file string."""
    # Call the function
    result = create_import_file_string(structured_raw_file=sample_songs_parent)
    
    # Check the result
    assert "Title: Test Song 1-(WITH-SPANISH)" in result
    assert "Title: Test Song 2-(WITH-SPANISH)" in result
    assert "Verse" in result
    assert "Chorus" in result
    assert "Verse line 1" in result
    assert "(Verso línea 1)" in result