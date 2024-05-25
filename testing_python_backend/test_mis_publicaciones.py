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

def test_get_mis_publicaciones_with_authentication():
    # Datos de inicio de sesión del usuario
    email = "janedoe@example.com"
    password = "password"

    # Obtener el token JWT
    token = get_access_token(email, password)

    # Realizar la solicitud GET para obtener las publicaciones del usuario actual con el token JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/mis_publicaciones", headers=headers)

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200  # Debe ser 200 (OK)

    # Verificar que la respuesta contenga una lista de publicaciones
    publicaciones = response.json()
    assert isinstance(publicaciones, list)  # La respuesta debe ser una lista

    # Opcional: Verificar que la lista no esté vacía (depende de los datos de prueba)
    assert len(publicaciones) > 0

    # Opcional: Verificar la estructura de una publicación (ajusta según tu modelo PublishProduct)
    for publicacion in publicaciones:
        assert "id_publish_prod" in publicacion
        assert "id_product" in publicacion
        assert "id_user" in publicacion
        assert "product_name" in publicacion
        assert "unit_value" in publicacion
        assert "quantity" in publicacion
        assert "description" in publicacion
        assert "location" in publicacion
        assert "image" in publicacion
