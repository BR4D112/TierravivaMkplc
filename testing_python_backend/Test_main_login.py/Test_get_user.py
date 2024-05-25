from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_user_info():
    # Supongamos que tienes un usuario con ID 2 en tu base de datos
    user_id = 3
    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    # Aquí puedes agregar más aserciones para verificar los datos del usuario devuelto
    assert response.json()["id_user"] == user_id
    assert response.json()["email"] == "juan.perez@example.com"
    # Agrega más aserciones según la estructura de tus datos de usuario
