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


# Prueba para crear y agregar un carrito con productos con autenticación
def test_create_and_add_to_cart_with_authentication():
    # Datos de inicio de sesión del usuario
    email = "janedoe@example.com"
    password = "password"

    # Obtener el token JWT
    token = get_access_token(email, password)

    # Datos de los productos a agregar al carrito
    cart_items = [
        {"id_publish_prod": 1, "quantity": 2},  # Actualiza con los IDs de los productos y sus cantidades
        {"id_publish_prod": 2, "quantity": 1}
    ]

    # Realizar la solicitud POST para crear y agregar al carrito con el token JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/crear_y_agregar_carrito", json={"cart_items": cart_items}, headers=headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200  # Debe ser 200 (OK)

    # Verificar que el mensaje de respuesta sea el esperado
    assert response.json()["mensaje"] == "Carrito creado y productos agregados exitosamente"
