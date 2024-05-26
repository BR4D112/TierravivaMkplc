import pytest
import requests

# Definir la URL base de tu API
BASE_URL = "http://localhost:8000"  # Actualiza con la URL correcta de tu API


# Función para obtener el token JWT
def get_access_token(email, password):
    login_data = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to obtain access token")


# Prueba para eliminar un producto con autenticación
def test_delete_product_with_authentication():
    # Datos de inicio de sesión del usuario
    email = "fercho@example.com"
    password = "456"

    # Obtener el token JWT
    token = get_access_token(email, password)

    # Realizar la solicitud DELETE para eliminar el producto con el token JWT
    product_id = 1012  # Actualiza con el ID del producto que deseas eliminar
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200  # Debe ser 200 (OK)

    # Verificar que el mensaje de respuesta sea el esperado
    assert response.json()["message"] == "Producto eliminado exitosamente"
