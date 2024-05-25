import pytest
import requests
from pydantic import BaseModel

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


# Clase para el modelo de datos de entrada para eliminar un producto del carrito
class DeleteItem(BaseModel):
    id_publish_prod: int


# Prueba para eliminar un producto del carrito con autenticación
def test_delete_product_from_cart_with_authentication():
    # Datos de inicio de sesión del usuario
    email = "janedoe@example.com"
    password = "password"

    # Obtener el token JWT
    token = get_access_token(email, password)

    # Datos del producto que se va a eliminar del carrito
    delete_item = DeleteItem(id_publish_prod=6)  # Actualiza con el ID del producto que deseas eliminar del carrito

    # Realizar la solicitud DELETE para eliminar un producto del carrito con el token JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/eliminar_producto_del_carrito", json=delete_item.dict(), headers=headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200  # Debe ser 200 (OK)

    # Verificar que el mensaje de respuesta sea el esperado
    assert response.json()["mensaje"] == "Producto eliminado del carrito y cantidad actualizada exitosamente."
