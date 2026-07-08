# Example: Test fee calculation
import httpx


def test_fee_calculation():
    payload = {"distance_km": 5, "time_minutes": 10}
    response = httpx.post("http://localhost:8000/calculate-fee", json=payload)
    assert response.status_code == 200
    assert "fee" in response.json()