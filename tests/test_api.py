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

def test_predict_endpoint_returns_model_state():
    response = client.post("/predict", json={"password": "Abc123!@"})
    assert response.status_code == 200
    data = response.json()
    assert "available" in data
    assert "features" in data
    assert data["features"]["length"] == 8

def test_health_endpoint_returns_operational_state():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_available" in data
    assert "feedback" in data

def test_model_status_endpoint_returns_model_path():
    response = client.get("/model/status")

    assert response.status_code == 200
    data = response.json()
    assert "available" in data
    assert data["model_path"].endswith("password_strength_model.joblib")

def test_model_reload_endpoint_returns_model_state():
    response = client.post("/model/reload")

    assert response.status_code == 200
    data = response.json()
    assert "available" in data
    assert data["model_path"].endswith("password_strength_model.joblib")

def test_model_metadata_endpoint_returns_training_metadata():
    response = client.get("/model/metadata")

    assert response.status_code == 200
    data = response.json()
    assert data["available"] is True
    assert data["metadata"]["experiment_name"] == "password-security-analyzer"
    assert data["metadata"]["accuracy"] >= 0

def test_feedback_endpoint_saves_user_feedback():
    response = client.post(
        "/feedback",
        json={
            "password": "Abc123!@",
            "is_correct": True,
            "comment": "prediction looked reasonable",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["saved"] is True
    assert data["feedback"]["password_length"] == 8
