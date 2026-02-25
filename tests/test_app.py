from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_initial_data():
    # Arrange: client already created
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_and_duplicate():
    # Arrange
    activity = "Science Club"
    email = "test@student.edu"

    # Act - first signup
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp1.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act - duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp2.status_code == 400


def test_remove_participant_and_not_found():
    # Arrange
    activity = "Debate Team"
    email = "remove@test.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act - remove existing
    resp1 = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert resp1.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]

    # Act - remove again
    resp2 = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert resp2.status_code == 404
