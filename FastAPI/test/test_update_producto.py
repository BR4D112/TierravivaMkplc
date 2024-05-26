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


# Prueba para actualizar un producto con autenticación
def test_update_product_with_authentication():
    # Datos de inicio de sesión del usuario
    email = "janedoe@example.com"
    password = "password"

    # Obtener el token JWT
    token = get_access_token(email, password)

    # ID del producto a actualizar
    product_id = 1  # Supongamos que queremos actualizar el producto con ID 1

    # Nuevos datos del producto
    updated_product_data = {
        "id_categorie": 2,
        "id_measure_prod": 3,
        "product_name": "Nuevo nombre de producto",
        "unit_value": 15.75,
        "quantity": 200,
        "description": "Nueva descripción del producto",
        "location": "Nueva ubicación del producto",
        "image": "Nueva URL de imagen"
    }

    # Realizar la solicitud PUT para actualizar el producto con el token JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=updated_product_data, headers=headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200  # Debe ser 200 (OK)

    # Verificar que el mensaje de respuesta sea el esperado
    assert response.json()["message"] == "Producto actualizado exitosamente"


# Si deseas realizar más pruebas, puedes agregarlas aquí

