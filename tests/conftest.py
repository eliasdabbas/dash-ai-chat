import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_directory:
        yield temp_directory


@pytest.fixture
def mock_openai_env():
    """Mock OpenAI API key environment variable."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield


@pytest.fixture
def app_with_temp_dir(temp_dir):
    """Provide a DashAIChat app instance with a temporary directory."""
    from dash_ai_chat import DashAIChat

    return DashAIChat(base_dir=temp_dir)
