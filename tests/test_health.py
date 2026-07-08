# Example: Test health endpoint
import httpx


def test_health():
    response = httpx.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}