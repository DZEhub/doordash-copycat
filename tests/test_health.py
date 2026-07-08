# Example: Test health endpoint
import httpx

# test for @app.post("/calculate-fee/")
def test_health():
    response = httpx.get("http://localhost:8080/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # pass