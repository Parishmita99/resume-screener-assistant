
import pytest
from unittest.mock import patch, MagicMock

from ai_engine import analyze_resume
from pydantic import ValidationError


def test_empty_job_description():
    with pytest.raises(ValueError, match="Job description"):
        analyze_resume("", "Python Developer resume")


def test_empty_resume():
    with pytest.raises(ValueError, match="Resume"):
        analyze_resume("Python Developer required", "")


@patch("ai_engine.API_KEY", None)
def test_missing_api_key():
    with pytest.raises(ValueError, match="API key"):
        analyze_resume("Python Developer required", "Python Developer")


@patch("ai_engine.API_KEY", "test-key")
@patch("ai_engine.genai.Client")
def test_malformed_ai_response(mock_client):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance

    mock_response = MagicMock()
    mock_response.text = '{"candidate_name": "Rahul", "match_score": 150}'
    mock_instance.models.generate_content.return_value = mock_response

    with pytest.raises(RuntimeError, match="Resume analysis failed"):
        analyze_resume("Python Developer required", "Python Developer")
