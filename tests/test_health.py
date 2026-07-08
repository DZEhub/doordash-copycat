# Example: Test health endpoint
import httpx


# test for @app.get("/status/")
def test_health():
    response = httpx.get("http://localhost:8080/status/")  # Fixed endpoint from /health to /status/
    assert response.status_code == 200
    assert response.json() == {"status": "Service is up and running"}  # Fixed response value
    # pass