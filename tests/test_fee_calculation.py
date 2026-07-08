# Example: Test fee calculation
import httpx


# test for @app.post("/calculate-fee/")
def test_fee_calculation():
    payload = {"distance_km": 5, "weight_kg": 2}  # Fixed payload with correct keys
    response = httpx.post("http://localhost:8080/calculate-fee/", json=payload)  # Fixed endpoint with trailing slash
    assert response.status_code == 200
    assert "delivery_fee" in response.json()  # Fixed response key
    # pass