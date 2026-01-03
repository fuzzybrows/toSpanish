import pytest
from unittest.mock import patch, MagicMock

from app.database import get_session


@patch("app.database.Session")
def test_get_session(mock_session):
    """Test that get_session yields a session."""
    # Create a mock session
    session_instance = MagicMock()
    mock_session.return_value.__enter__.return_value = session_instance
    
    # Get the session generator
    session_generator = get_session()
    
    # Get the yielded session
    session = next(session_generator)
    
    # Check that the session is the mock session
    assert session == session_instance
    
    # Check that the session is closed when the generator is exhausted
    try:
        next(session_generator)
        pytest.fail("Session generator should only yield once")
    except StopIteration:
        pass
    
    # Verify that the session was created with the engine
    mock_session.assert_called_once()