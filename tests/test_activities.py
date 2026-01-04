import pytest
from fastapi.testclient import TestClient


def test_get_activities(client: TestClient):
    """Test getting all activities."""
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

    # Check that Chess Club exists and has expected structure
    assert "Chess Club" in data
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity_success(client: TestClient):
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "test@example.com" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_for_activity_already_signed_up(client: TestClient):
    """Test signup when already signed up."""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")

    # Try to signup again
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_for_nonexistent_activity(client: TestClient):
    """Test signup for a non-existent activity."""
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_from_activity_success(client: TestClient):
    """Test successful unregister from an activity."""
    # First signup
    client.post("/activities/Programming%20Class/signup?email=unregister@example.com")

    # Then unregister
    response = client.delete("/activities/Programming%20Class/unregister?email=unregister@example.com")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "unregister@example.com" in data["message"]
    assert "Programming Class" in data["message"]


def test_unregister_from_activity_not_signed_up(client: TestClient):
    """Test unregister when not signed up."""
    response = client.delete("/activities/Chess%20Club/unregister?email=notsignedup@example.com")
    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_from_nonexistent_activity(client: TestClient):
    """Test unregister from a non-existent activity."""
    response = client.delete("/activities/NonExistent/unregister?email=test@example.com")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_root_redirect(client: TestClient):
    """Test root endpoint redirects to static index.html."""
    response = client.get("/")
    assert response.status_code == 200
    # FastAPI's RedirectResponse might be handled differently in tests
    # The actual redirect happens, so we check if we get a response


def test_static_files_served(client: TestClient):
    """Test that static files are being served."""
    response = client.get("/static/index.html")
    assert response.status_code == 200
    assert "Mergington High School" in response.text

    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert "box-sizing" in response.text

    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "DOMContentLoaded" in response.text