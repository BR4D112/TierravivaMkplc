from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_user():
    # Datos de usuario existente en el sistema
    user_credentials = {
        "email": "janedoe@example.com",
        "password": "password"
    }

    # Enviar solicitud POST al endpoint de login
    response = client.post("/login", json=user_credentials)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200

    # Verificar que se recibió un token de acceso en la respuesta
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
