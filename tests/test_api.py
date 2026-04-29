from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_strong_password():
    response = client.post("/analyze", json={"password": "Abc123!@"})
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "strong"

def test_analyze_weak_password():
    response = client.post("/analyze", json={"password": "abc"})
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "weak"

def test_analyze_medium_password():
    response = client.post("/analyze", json={"password": "abc12345"})
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "medium"