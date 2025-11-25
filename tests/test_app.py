import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email} for {activity}" in data["message"]
    # Check participant added
    response2 = client.get("/activities")
    assert email in response2.json()[activity]["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_participant():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # First, sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Now, unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "eliminado" in response.json()["message"] or "removed" in response.json()["message"].lower()
    # Check participant removed
    response2 = client.get("/activities")
    assert email not in response2.json()[activity]["participants"]
