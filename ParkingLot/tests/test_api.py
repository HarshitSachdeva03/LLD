def test_park_vehicle_success(client):
    """Tests a successful parking allocation."""
    payload = {
        "license_plate": "KA-01-HH-1234",
        "vehicle_type": "CAR"
    }
    response = client.post("/park", json=payload)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Parked successfully"
    assert "spot_id" in response.json()

def test_park_vehicle_invalid_type(client):
    """Tests Pydantic's automatic 422 validation error."""
    payload = {
        "license_plate": "XYZ-999",
        "vehicle_type": "HELICOPTER" # Invalid Enum
    }
    response = client.post("/park", json=payload)
    
    # FastAPI automatically rejects invalid data before hitting our logic
    assert response.status_code == 422