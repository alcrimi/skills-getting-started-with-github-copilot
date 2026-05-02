from fastapi.testclient import TestClient
from src.app import app, activities
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: reset del database in memoria prima di ogni test
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Test Chess Club",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alice@mergington.edu"]
        },
        "Programming Class": {
            "description": "Test Programming Class",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["bob@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Test Art Workshop",
            "schedule": "Mondays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": []
        }
    })


def test_get_activities():
    # Arrange: stato iniziale fornito dalla fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Art Workshop" in data


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "alice@mergington.edu"  # già iscritto
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_success():
    # Arrange
    email = "bob@mergington.edu"
    # Act
    response = client.delete("/activities/Programming Class/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    # Act
    response = client.delete("/activities/Art Workshop/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
