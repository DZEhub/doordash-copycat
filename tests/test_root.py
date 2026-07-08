# Example: Test health endpoint
import httpx


# test for @app.get("/")
def test_root():
    response = httpx.get("http://localhost:8080/")
    assert response.status_code == 200
    assert "message" in response.json()
    # pass


# test for @app.get("/status/")
def test_status():
    response = httpx.get("http://localhost:8080/status/")
    assert response.status_code == 200
    assert "status" in response.json()
    # pass


# Example: Test estimate time endpoint
def test_estimate_time():
    distance_km = 5
    response = httpx.get(f"http://localhost:8080/estimate-time/{distance_km}")
    assert response.status_code == 200
    assert "estimated_time" in response.json()
    # pass