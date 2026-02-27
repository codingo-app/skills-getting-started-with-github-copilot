from src.app import activities


def test_get_activities(client):
    # Arrange
    # (reset fixture already ran)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    email = "foo@school.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already present

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent"
    email = "a@b.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    assert email in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed(client):
    # Arrange
    activity = "Chess Club"
    email = "nobody@x.com"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Student not signed up for this activity"


def test_unregister_activity_not_found(client):
    # Arrange
    activity = "Ghost"
    email = "a@b.com"

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
