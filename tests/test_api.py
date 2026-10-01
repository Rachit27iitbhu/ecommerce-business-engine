from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_recommendations_endpoint(sample_df):
    with patch("backend.main.load_data", return_value=sample_df):
        response = client.get("/recommendations")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_data_quality_endpoint(sample_df):
    with patch("backend.main.load_data", return_value=sample_df):
        response = client.get("/data-quality")
        assert response.status_code == 200
        assert isinstance(response.json(), list)