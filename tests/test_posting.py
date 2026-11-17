from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    """Verify that the health/home endpoint is operational."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "OmniPost"
    assert data["status"] == "running"


def test_validation_missing_url():
    """Messages without any CTA URL must return 422 Unprocessable Entity."""
    response = client.post(
        "/posting",
        json={"message": "This message has no URL at all in it"}
    )
    assert response.status_code == 422


def test_validation_multiple_urls():
    """Messages with more than 1 URL must be rejected with 422."""
    response = client.post(
        "/posting",
        json={"message": "Check https://example.com and also https://google.com"}
    )
    assert response.status_code == 422


def test_validation_message_too_long():
    """Messages over 200 characters must be rejected with 422."""
    long_message = (
        "This message is intentionally created to exceed the maximum character limit "
        "defined in the specification for the OmniPost practical assessment project "
        "to ensure proper validation triggers https://example.com"
    )
    response = client.post(
        "/posting",
        json={"message": long_message}
    )
    assert response.status_code == 422


def test_validation_empty_message():
    """Empty messages must be rejected."""
    response = client.post(
        "/posting",
        json={"message": "   "}
    )
    assert response.status_code == 422