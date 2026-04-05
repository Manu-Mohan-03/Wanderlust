import pytest

TEST_DATA = {
  "user_id": 1,
  "name": "My Summer Trip",
  "trip_legs": [
    {
      "leg_no": 1,
      "mode": "flight",
      "origin_city": "Berlin",
      "destination_city": "Paris",
      "leg_start": "2026-04-01T10:00:00",
      "leg_stop": "2026-04-01T12:00:00",
      "flight": {
        "flight_id": "LH123"
      }
    },
    {
      "leg_no": 2,
      "mode": "flight",
      "origin_city": "Paris",
      "destination_city": "Madrid",
      "leg_start": "2026-04-03T09:00:00",
      "leg_stop": "2026-04-03T11:30:00",
      "flight": {
        "flight_id": "AF456"
      }
    }
  ]
}

# from fastapi.testclient import TestClient
# from main import app  # adjust import to your app location

# client = TestClient(app)

# # Fake DB session
# def override_get_db():
#     class FakeDB:
#         def commit(self): pass
#         def add(self, obj): pass
#         def refresh(self, obj): pass
#     yield FakeDB()

# app.dependency_overrides[get_db] = override_get_db

def test_create_trip_success():
    pass
    # response = client.post("/trip", json=TEST_DATA)
    #
    # assert response.status_code == 200
    #
    # data = response.json()
    #
    # # Adjust these assertions based on your TripOut model
    # assert data is not None
    # assert data["name"] == "My Summer Trip"
    # assert data["user_id"] == 1

def test_create_trip_invalid_payload():
    pass
    # payload = {
    #     "user_id": 1,
    #     # missing trip_legs → should fail
    # }
    #
    # response = client.post("/trip", json=payload)
    #
    # assert response.status_code == 422