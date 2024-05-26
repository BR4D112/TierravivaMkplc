from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={
        "person": {
            "first_name": "Jane",
            "last_name": "Doe",
            "doc_type": "DNI",
            "doc_number": "87654321",
            "phone_number": "987654321",
            "location": "Anywhere"
        },
        "email": "janedoe@example.com",
        "credit_number": "6543-2109-8765-4321",
        "password": "password"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "janedoe@example.com"
