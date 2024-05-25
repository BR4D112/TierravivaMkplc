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


# Prueba para registrar un producto con autenticación
def test_register_product_with_authentication():
    # Datos de inicio de sesión del usuario
    email = "janedoe@example.com"
    password = "password"

    # Obtener el token JWT
    token = get_access_token(email, password)

    # Datos del producto a registrar
    product_data = {
        "id_categorie": 1,
        "id_measure_prod": 1,
        "product_name": "Producto de prueba",
        "unit_value": 10.5,
        "quantity": 100,
        "description": "Descripción del producto de prueba",
        "location": "Ubicación del producto",
        "image": "URL_de_la_imagen"
    }

    # Realizar la solicitud POST para registrar el producto con el token JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/product_register", json=product_data, headers=headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 201  # Debe ser 201 (creado)

    # Verificar que el mensaje de respuesta sea el esperado
    assert response.json()["message"] == "Producto publicado exitosamente"


