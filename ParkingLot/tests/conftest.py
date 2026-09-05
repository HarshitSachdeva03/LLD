# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Creates a synchronous test client for our FastAPI app.
    Because this is in conftest.py, pytest automatically detects it 
    and makes it available to all test functions.
    """
    return TestClient(app)