from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import pyodbc
from starlette import status

from controllers.auth_controller import get_current_user, SECRET_KEY, ALGORITHM, TokenData
from models.product import ProductCreate, ProductUpdate, Product
from services.db import get_db_connection



import secrets
import smtplib
import string
from email.mime.text import MIMEText
from typing import List



import secrets
import smtplib
import string
from email.mime.text import MIMEText
from typing import List


import uvicorn
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
import pyodbc
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from starlette import status
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()
#   Crear  producto

@router.post("/", status_code=201)
def create_product(
    product: ProductCreate,
    current_user: dict = Depends(get_current_user),
    db: pyodbc.Connection = Depends(get_db_connection)
):
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO PRODUCTS (
            ID_CATEGORIE, ID_MEASURE_PROD, PRODUCT_NAME, UNIT_VALUE,
            QUANTITY, DESCRIPTION, LOCATION, IMAGE
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product.id_categorie, product.id_measure_prod, product.product_name,
            product.unit_value, product.quantity, product.description,
            product.location, product.image
        )
    )
    db.commit()

    product_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

    cursor.execute(
        "INSERT INTO PUBLISH_PRODUCT (ID_PRODUCT, ID_USER) VALUES (?, ?)",
        (product_id, current_user["id_user"])
    )
    db.commit()
    cursor.close()

    return {"message": "Producto publicado exitosamente"}
#actualizar   producto
@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: dict = Depends(get_current_user),
    db: pyodbc.Connection = Depends(get_db_connection)
):
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE PRODUCTS
        SET ID_CATEGORIE = ?, ID_MEASURE_PROD = ?, PRODUCT_NAME = ?,
            UNIT_VALUE = ?, QUANTITY = ?, DESCRIPTION = ?, LOCATION = ?, IMAGE = ?
        WHERE ID_PRODUCT = ?
        """,
        (
            product.id_categorie, product.id_measure_prod, product.product_name,
            product.unit_value, product.quantity, product.description,
            product.location, product.image, product_id
        )
    )
    db.commit()
    cursor.close()

    return {"message": "Producto actualizado exitosamente"}
#  Eliminar  producto
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user: dict = Depends(get_current_user),
    db: pyodbc.Connection = Depends(get_db_connection)
):
    cursor = db.cursor()

    # Verificar si el producto existe y si fue publicado por el usuario actual o si el usuario es administrador
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM PUBLISH_PRODUCT
        WHERE ID_PRODUCT = ? AND (ID_USER = ? OR (SELECT IS_ADMIN FROM USERS WHERE ID_USER = ?) = 1)
        """,
        (product_id, current_user["id_user"], current_user["id_user"])
    )
    count = cursor.fetchone()[0]

    if count == 0:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este producto")

    # Eliminar los registros relacionados en PRODUCTS_ADDED
    cursor.execute(
        "DELETE FROM PRODUCTS_ADDED WHERE ID_PUBLISH_PROD = ?",
        (product_id,)
    )

    # Eliminar el registro en PUBLISH_PRODUCT
    cursor.execute(
        "DELETE FROM PUBLISH_PRODUCT WHERE ID_PRODUCT = ? AND ID_USER = ?",
        (product_id, current_user["id_user"])
    )

    db.commit()
    cursor.close()

    return {"message": "Producto eliminado exitosamente"}





# Función para crear un carrito de compras
@router.post("/crear_carrito")
def crear_carrito(current_user=Depends(get_current_user), db=Depends(get_db_connection)):
    cursor = db.cursor()

    # Verificar si ya existe un carrito para el usuario actual
    cursor.execute("""
        SELECT ID_SHOP_CAR
        FROM SHOPPING_CARS
        WHERE ID_USER = ?
    """, (current_user["id_user"],))
    existing_cart = cursor.fetchone()

    if existing_cart:
        cursor.close()
        return {"mensaje": "Ya existe un carrito para el usuario actual"}

    # Si no existe un carrito, crear uno nuevo
    cursor.execute("""
        INSERT INTO SHOPPING_CARS (ID_USER)
        VALUES (?)
    """, (current_user["id_user"],))
    db.commit()

    cursor.execute("""
        SELECT ID_SHOP_CAR
        FROM SHOPPING_CARS
        WHERE ID_USER = ?
    """, (current_user["id_user"],))
    cart_id = cursor.fetchone()[0]

    cursor.close()
    return {"mensaje": "Carrito creado exitosamente", "id_carrito": cart_id}


from typing import List
from pydantic import BaseModel

class CartItem(BaseModel):
    id_publish_prod: int
    quantity: int

class CartItems(BaseModel):
    cart_items: List[CartItem]

# Función para agregar productos al carrito
@router.post("/agregar_al_carrito")
def agregar_al_carrito(items: CartItems, current_user=Depends(get_current_user), db=Depends(get_db_connection)):
    cursor = db.cursor()

    # Verificar si el usuario tiene un carrito de compras
    cursor.execute("""
        SELECT ID_SHOP_CAR
        FROM SHOPPING_CARS
        WHERE ID_USER = ?
    """, (current_user["id_user"],))
    shopping_cart = cursor.fetchone()

    if not shopping_cart:
        # Si el usuario no tiene un carrito de compras, crear uno nuevo
        cursor.execute("""
            INSERT INTO SHOPPING_CARS (ID_USER)
            VALUES (?)
        """, (current_user["id_user"],))
        db.commit()
        shopping_cart_id = cursor.lastrowid
    else:
        shopping_cart_id = shopping_cart[0]

    for item in items.cart_items:
        # Verificar si el producto ya está en el carrito
        cursor.execute("""
            SELECT *
            FROM PRODUCTS_ADDED
            WHERE ID_SHOP_CAR = ?
              AND ID_PUBLISH_PROD = ?
        """, (shopping_cart_id, item.id_publish_prod))
        existing_item = cursor.fetchone()

        if existing_item:
            # Si el producto ya está en el carrito, actualizar la cantidad
            cursor.execute("""
                UPDATE PRODUCTS_ADDED
                SET QUANTITY = QUANTITY + ?
                WHERE ID_SHOP_CAR = ?
                  AND ID_PUBLISH_PROD = ?
            """, (item.quantity, shopping_cart_id, item.id_publish_prod))
        else:
            # Si el producto no está en el carrito, crear un nuevo registro
            cursor.execute("""
                INSERT INTO PRODUCTS_ADDED (ID_SHOP_CAR, ID_PUBLISH_PROD, QUANTITY)
                VALUES (?, ?, ?)
            """, (shopping_cart_id, item.id_publish_prod, item.quantity))

    db.commit()
    cursor.close()
    return {"mensaje": "Productos agregados al carrito"}


# Función para obtener la lista de productos por categoría
@router.get("/categoria/{categoria_id}")
def get_products_by_category(categoria_id: int, db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()

    # Consulta para obtener los productos en la categoría especificada
    cursor.execute("""
        SELECT PRODUCT_NAME, UNIT_VALUE, QUANTITY, DESCRIPTION, LOCATION, IMAGE
        FROM PRODUCTS
        WHERE ID_CATEGORIE = ?
    """, (categoria_id,))
    products = cursor.fetchall()

    cursor.close()

    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos en esta categoría")

    # Formatear los resultados
    formatted_products = []
    for product in products:
        formatted_product = {
            "product_name": product[0],
            "unit_value": product[1],
            "quantity": product[2],
            "description": product[3],
            "location": product[4],
            "image": product[5]
        }
        formatted_products.append(formatted_product)

    return formatted_products

from pydantic import BaseModel

class ProductPublisherName(BaseModel):
    first_name: str
    last_name: str

class ProductInfo(BaseModel):
    product_name: str
    unit_value: float
    quantity: int
    description: str
    location: str
    image: str
    user_name: ProductPublisherName  # Cambiar el nombre del campo


from fastapi import HTTPException

@router.get("/{product_id}", response_model=ProductInfo)  # Especificar el modelo de respuesta
async def get_product_publisher_name(product_id: int, db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()

    # Consulta SQL para obtener la información del producto y el nombre del editor
    cursor.execute("""
        SELECT p.PRODUCT_NAME, p.UNIT_VALUE, p.QUANTITY, p.DESCRIPTION, p.LOCATION, p.IMAGE,
               per.FIRST_NAME, per.LAST_NAME
        FROM PRODUCTS p
        INNER JOIN PUBLISH_PRODUCT pp ON p.ID_PRODUCT = pp.ID_PRODUCT
        INNER JOIN USERS u ON pp.ID_USER = u.ID_USER
        INNER JOIN PERSONS per ON u.ID_PERSON = per.ID_PERSON
        WHERE p.ID_PRODUCT = ?
    """, (product_id,))
    product_info = cursor.fetchone()

    cursor.close()

    if not product_info:
        raise HTTPException(status_code=404, detail="No se encontró el producto")

    # Formatear los resultados en un diccionario
    formatted_product_info = {
        "product_name": product_info[0],
        "unit_value": product_info[1],
        "quantity": product_info[2],
        "description": product_info[3],
        "location": product_info[4],
        "image": product_info[5],
        "user_name": {
            "first_name": product_info[6],
            "last_name": product_info[7]
        }
    }

    return formatted_product_info

@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: dict = Depends(get_current_user),
    db: pyodbc.Connection = Depends(get_db_connection)
):
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE PRODUCTS
        SET ID_CATEGORIE = ?, ID_MEASURE_PROD = ?, PRODUCT_NAME = ?,
            UNIT_VALUE = ?, QUANTITY = ?, DESCRIPTION = ?, LOCATION = ?, IMAGE = ?
        WHERE ID_PRODUCT = ?
        """,
        (
            product.id_categorie, product.id_measure_prod, product.product_name,
            product.unit_value, product.quantity, product.description,
            product.location, product.image, product_id
        )
    )
    db.commit()
    cursor.close()

    return {"message": "Producto actualizado exitosamente"}




@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: dict = Depends(get_current_user),
    db: pyodbc.Connection = Depends(get_db_connection())
):
    cursor = db.cursor()

    # Verificar si el producto existe y si fue publicado por el usuario actual o si el usuario es administrador
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM PUBLISH_PRODUCT
        WHERE ID_PRODUCT = ? AND (ID_USER = ? OR (SELECT IS_ADMIN FROM USERS WHERE ID_USER = ?) = 1)
        """,
        (product_id, current_user["id_user"], current_user["id_user"])
    )
    count = cursor.fetchone()[0]

    if count == 0:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este producto")

    # Eliminar los registros relacionados en PRODUCTS_ADDED
    cursor.execute(
        "DELETE FROM PRODUCTS_ADDED WHERE ID_PUBLISH_PROD = ?",
        (product_id,)
    )

    # Eliminar el registro en PUBLISH_PRODUCT
    cursor.execute(
        "DELETE FROM PUBLISH_PRODUCT WHERE ID_PRODUCT = ? AND ID_USER = ?",
        (product_id, current_user["id_user"])
    )

    db.commit()
    cursor.close()

    return {"message": "Producto eliminado exitosamente"}



@router.get("/categorie/{categoria_id}")
def get_products_by_category(categoria_id: int, db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()

    # Consulta para obtener los productos en la categoría especificada
    cursor.execute("""
        SELECT PRODUCT_NAME, UNIT_VALUE, QUANTITY, DESCRIPTION, LOCATION, IMAGE
        FROM PRODUCTS
        WHERE ID_CATEGORIE = ?
    """, (categoria_id,))
    products = cursor.fetchall()

    cursor.close()

    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos en esta categoría")

    # Formatear los resultados
    formatted_products = []
    for product in products:
        formatted_product = {
            "product_name": product[0],
            "unit_value": product[1],
            "quantity": product[2],
            "description": product[3],
            "location": product[4],
            "image": product[5]
        }
        formatted_products.append(formatted_product)

    return formatted_products



@router.get("/products_by_categorie", response_model=list[Product])
def get_products_by_categorie(id_categorie: int, db: pyodbc.Connection = Depends(get_db_connection())):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT ID_PRODUCT, ID_CATEGORIE, ID_MEASURE_PROD, PRODUCT_NAME, UNIT_VALUE, QUANTITY, DESCRIPTION, LOCATION, IMAGE
        FROM PRODUCTS
        WHERE ID_CATEGORIE = ?
        """, id_categorie
    )
    rows = cursor.fetchall()
    products = []
    for row in rows:
        product = Product(
            id_product=row[0],
            id_categorie=row[1],
            id_measure_prod=row[2],
            product_name=row[3],
            unit_value=row[4],
            quantity=row[5],
            description=row[6],
            location=row[7],
            image=row[8]
        )
        products.append(product)
    cursor.close()
    return products

@router.get("/products/name/{product_name}", response_model=list[Product])
def get_products_by_name(product_name: str, db: pyodbc.Connection = Depends(get_db_connection())):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT ID_PRODUCT, ID_CATEGORIE, ID_MEASURE_PROD, PRODUCT_NAME, UNIT_VALUE, QUANTITY, DESCRIPTION, LOCATION, IMAGE
        FROM PRODUCTS
        WHERE PRODUCT_NAME LIKE ?
        """,
        ('%' + product_name + '%',)
    )
    rows = cursor.fetchall()
    products = []
    for row in rows:
        product = Product(
            id_product=row[0],
            id_categorie=row[1],
            id_measure_prod=row[2],
            product_name=row[3],
            unit_value=row[4],
            quantity=row[5],
            description=row[6],
            location=row[7],
            image=row[8]
        )
        products.append(product)
    cursor.close()
    return products


# Función para obtener al usuario actual (ejemplo básico)
async def get_current_user(token: str = Depends(oauth2_scheme), db: pyodbc.Connection = Depends(get_db_connection)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.JWTError:
        raise credentials_exception

    # Obtener la información del usuario de la base de datos usando el correo electrónico
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT id_user
        FROM users
        WHERE email = ?
        """,
        (token_data.email,)
    )
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_id = result[0]
    current_user = {"id_user": user_id}
    return current_user


@router.post("/eliminar_del_carrito")
def eliminar_del_carrito(item: CartItem, current_user=Depends(get_current_user), db=Depends(get_db_connection)):
    cursor = db.cursor()

    # Verificar si el usuario tiene un carrito de compras
    cursor.execute("""
        SELECT ID_SHOP_CAR
        FROM SHOPPING_CARS
        WHERE ID_USER = ?
    """, (current_user["id_user"],))
    shopping_cart = cursor.fetchone()

    if not shopping_cart:
        cursor.close()
        raise HTTPException(status_code=404, detail="Carrito de compras no encontrado")

    shopping_cart_id = shopping_cart[0]

    # Verificar si el producto está en el carrito
    cursor.execute("""
        SELECT QUANTITY
        FROM PRODUCTS_ADDED
        WHERE ID_SHOP_CAR = ?
          AND ID_PUBLISH_PROD = ?
    """, (shopping_cart_id, item.id_publish_prod))
    existing_item = cursor.fetchone()

    if not existing_item:
        cursor.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

    item_quantity = existing_item[0]

    # Eliminar el producto del carrito
    cursor.execute("""
        DELETE FROM PRODUCTS_ADDED
        WHERE ID_SHOP_CAR = ?
          AND ID_PUBLISH_PROD = ?
    """, (shopping_cart_id, item.id_publish_prod))

    # Obtener el ID_PRODUCT a partir de ID_PUBLISH_PROD
    cursor.execute("""
        SELECT P.ID_PRODUCT
        FROM PRODUCTS P
        JOIN PUBLISH_PRODUCT PP ON P.ID_PRODUCT = PP.ID_PRODUCT
        WHERE PP.ID_PUBLISH_PROD = ?
    """, (item.id_publish_prod,))
    result = cursor.fetchone()

    if result:
        product_id = result[0]

        # Obtener la cantidad actual del producto
        cursor.execute("""
            SELECT QUANTITY
            FROM PRODUCTS
            WHERE ID_PRODUCT = ?
        """, (product_id,))
        current_quantity = cursor.fetchone()[0]

        updated_quantity = current_quantity + item_quantity

        # Actualizar la cantidad del producto en la tabla PRODUCTS
        cursor.execute("""
            UPDATE PRODUCTS
            SET QUANTITY = ?
            WHERE ID_PRODUCT = ?
        """, (updated_quantity, product_id))
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado en la base de datos")

    db.commit()  # Confirmar los cambios

    cursor.close()
    return {"mensaje": "Producto eliminado del carrito"}


class UserInfo(BaseModel):
    email: str
    first_name: str
    last_name: str
    doc_type: str
    doc_number: str
    phone_number: str
    location: str


@router.get("/users/me", response_model=UserInfo)
def get_current_user_info(current_user: dict = Depends(get_current_user), db=Depends(get_db_connection)):
    cursor = db.cursor()
    user_id = current_user["id_user"]

    cursor.execute(
        """
        SELECT U.EMAIL, P.FIRST_NAME, P.LAST_NAME, P.DOC_TYPE, P.DOC_NUMBER, P.PHONE_NUMBER, P.LOCATION
        FROM USERS U
        JOIN PERSONS P ON U.ID_PERSON = P.ID_PERSON
        WHERE U.ID_USER = ?
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    cursor.close()

    if row:
        user_info = UserInfo(
            email=row[0],
            first_name=row[1],
            last_name=row[2],
            doc_type=row[3],
            doc_number=row[4],
            phone_number=row[5],
            location=row[6]
        )
        return user_info

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Dependencias para obtener el usuario actual y la sesión de la base de datos

# Modelo Pydantic para la respuesta
class ProductInCart(BaseModel):
    id_publish_prod: int
    product_name: str
    quantity: int


@router.get("/carrito_de_compras", response_model=List[ProductInCart])
def mostrar_carrito(current_user=Depends(get_current_user), db=Depends(get_db_connection)):
    cursor = db.cursor()

    try:
        # Verificar si el usuario tiene un carrito de compras
        cursor.execute("""
            SELECT ID_SHOP_CAR
            FROM SHOPPING_CARS
            WHERE ID_USER = ?
        """, (current_user["id_user"],))
        shopping_cart = cursor.fetchone()

        if not shopping_cart:
            raise HTTPException(status_code=404, detail="Carrito de compras no encontrado")

        shopping_cart_id = shopping_cart[0]

        # Obtener los productos en el carrito
        cursor.execute("""
            SELECT PA.ID_PUBLISH_PROD, P.PRODUCT_NAME, PA.QUANTITY
            FROM PRODUCTS_ADDED PA
            JOIN PUBLISH_PRODUCT PP ON PA.ID_PUBLISH_PROD = PP.ID_PUBLISH_PROD
            JOIN PRODUCTS P ON PP.ID_PRODUCT = P.ID_PRODUCT
            WHERE PA.ID_SHOP_CAR = ?
        """, (shopping_cart_id,))
        productos_en_carrito = cursor.fetchall()

        if not productos_en_carrito:
            raise HTTPException(status_code=404, detail="No hay productos en el carrito")

        productos = []
        for producto in productos_en_carrito:
            productos.append(ProductInCart(
                id_publish_prod=producto[0],
                product_name=producto[1],
                quantity=producto[2]
            ))

        return productos

    finally:

        cursor.close()


from typing import Optional


class CartItem(BaseModel):
    id_publish_prod: int
    quantity: Optional[int] = None


class DeleteItem(BaseModel):
    id_publish_prod: int


@router.delete("/eliminar_producto_del_carrito")
def eliminar_producto_del_carrito(item: DeleteItem, current_user=Depends(get_current_user), db=Depends(get_db_connection())):
    cursor = db.cursor()

    try:
        # Obtener el ID del carrito del usuario actual
        cursor.execute("""
            SELECT ID_SHOP_CAR
            FROM SHOPPING_CARS
            WHERE ID_USER = ?
        """, (current_user["id_user"],))
        shopping_cart = cursor.fetchone()

        if not shopping_cart:
            raise HTTPException(status_code=404, detail="Carrito no encontrado.")

        shopping_cart_id = shopping_cart[0]

        # Obtener la cantidad del producto que se va a eliminar del carrito
        cursor.execute("""
            SELECT QUANTITY
            FROM PRODUCTS_ADDED
            WHERE ID_SHOP_CAR = ?
              AND ID_PUBLISH_PROD = ?
        """, (shopping_cart_id, item.id_publish_prod))
        product_in_cart = cursor.fetchone()

        if not product_in_cart:
            raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito.")

        quantity_to_return = product_in_cart[0]

        # Eliminar el producto del carrito
        cursor.execute("""
            DELETE FROM PRODUCTS_ADDED
            WHERE ID_SHOP_CAR = ?
              AND ID_PUBLISH_PROD = ?
        """, (shopping_cart_id, item.id_publish_prod))

        # Obtener el ID_PRODUCT a partir de ID_PUBLISH_PROD
        cursor.execute("""
            SELECT P.ID_PRODUCT
            FROM PRODUCTS P
            JOIN PUBLISH_PRODUCT PP ON P.ID_PRODUCT = PP.ID_PRODUCT
            WHERE PP.ID_PUBLISH_PROD = ?
        """, (item.id_publish_prod,))
        result = cursor.fetchone()

        if result:
            product_id = result[0]

            # Obtener la cantidad actual del producto
            cursor.execute("""
                SELECT QUANTITY
                FROM PRODUCTS
                WHERE ID_PRODUCT = ?
            """, (product_id,))
            current_quantity = cursor.fetchone()[0]

            # Actualizar la cantidad del producto en la tabla PRODUCTS
            new_quantity = current_quantity + quantity_to_return
            cursor.execute("""
                UPDATE PRODUCTS
                SET QUANTITY = ?
                WHERE ID_PRODUCT = ?
            """, (new_quantity, product_id))
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        cursor.close()

    return {"mensaje": "Producto eliminado del carrito y cantidad actualizada exitosamente."}


@router.post("/crear_y_agregar_carrito")
def crear_y_agregar_carrito(items: CartItems, current_user=Depends(get_current_user), db=Depends(get_db_connection())):
    cursor = db.cursor()

    try:
        # Verificar si ya existe un carrito para el usuario actual
        cursor.execute("""
            SELECT ID_SHOP_CAR
            FROM SHOPPING_CARS
            WHERE ID_USER = ?
        """, (current_user["id_user"],))
        existing_cart = cursor.fetchone()

        if existing_cart:
            shopping_cart_id = existing_cart[0]
        else:
            # Si no existe un carrito, crear uno nuevo
            cursor.execute("""
                INSERT INTO SHOPPING_CARS (ID_USER)
                VALUES (?)
            """, (current_user["id_user"],))
            db.commit()

            cursor.execute("""
                SELECT ID_SHOP_CAR
                FROM SHOPPING_CARS
                WHERE ID_USER = ?
            """, (current_user["id_user"],))
            shopping_cart_id = cursor.fetchone()[0]

        for item in items.cart_items:
            # Verificar si el producto ya está en el carrito
            cursor.execute("""
                SELECT *
                FROM PRODUCTS_ADDED
                WHERE ID_SHOP_CAR = ?
                  AND ID_PUBLISH_PROD = ?
            """, (shopping_cart_id, item.id_publish_prod))
            existing_item = cursor.fetchone()

            if existing_item:
                # Si el producto ya está en el carrito, actualizar la cantidad
                cursor.execute("""
                    UPDATE PRODUCTS_ADDED
                    SET QUANTITY = QUANTITY + ?
                    WHERE ID_SHOP_CAR = ?
                      AND ID_PUBLISH_PROD = ?
                """, (item.quantity, shopping_cart_id, item.id_publish_prod))
            else:
                # Si el producto no está en el carrito, crear un nuevo registro
                cursor.execute("""
                    INSERT INTO PRODUCTS_ADDED (ID_SHOP_CAR, ID_PUBLISH_PROD, QUANTITY)
                    VALUES (?, ?, ?)
                """, (shopping_cart_id, item.id_publish_prod, item.quantity))

            # Obtener el ID_PRODUCT a partir de ID_PUBLISH_PROD
            cursor.execute("""
                SELECT P.ID_PRODUCT
                FROM PRODUCTS P
                JOIN PUBLISH_PRODUCT PP ON P.ID_PRODUCT = PP.ID_PRODUCT
                WHERE PP.ID_PUBLISH_PROD = ?
            """, (item.id_publish_prod,))
            result = cursor.fetchone()

            if result:
                product_id = result[0]

                # Obtener la cantidad actual del producto
                cursor.execute("""
                    SELECT QUANTITY
                    FROM PRODUCTS
                    WHERE ID_PRODUCT = ?
                """, (product_id,))
                current_quantity = cursor.fetchone()[0]

                remaining_quantity = current_quantity - item.quantity

                if remaining_quantity >= 0:
                    # Actualizar la cantidad del producto en la tabla PRODUCTS
                    cursor.execute("""
                        UPDATE PRODUCTS
                        SET QUANTITY = ?
                        WHERE ID_PRODUCT = ?
                    """, (remaining_quantity, product_id))
                else:
                    # Si la cantidad restante es negativa, lanzar una excepción
                    cursor.close()
                    raise HTTPException(status_code=400,
                                        detail=f"Cantidad insuficiente para el producto ID {item.id_publish_prod}. Disponible: {current_quantity}, solicitado: {item.quantity}")

            else:
                # Si no se encuentra el producto, lanzar una excepción
                cursor.close()
                raise HTTPException(status_code=404, detail=f"Producto ID {item.id_publish_prod} no encontrado.")

        db.commit()  # Confirmar los cambios después de todas las operaciones

    except Exception as e:
        db.rollback()  # Deshacer todos los cambios si ocurre un error
        raise e

    finally:
        cursor.close()

    return {"mensaje": "Carrito creado y productos agregados exitosamente", "id_carrito": shopping_cart_id}


# Modelo para las publicaciones
class PublishProduct(BaseModel):
    id_publish_prod: int
    id_product: int
    id_user: int
    product_name: str
    unit_value: float
    quantity: float
    description: str
    location: str
    image: str


@router.get("/mis_publicaciones", response_model=List[PublishProduct])
def mostrar_mis_publicaciones(current_user=Depends(get_current_user), db=Depends(get_db_connection())):
    cursor = db.cursor()

    # Obtener las publicaciones del usuario actual
    cursor.execute("""
        SELECT 
            pp.ID_PUBLISH_PROD, 
            pp.ID_PRODUCT, 
            pp.ID_USER, 
            p.PRODUCT_NAME, 
            p.UNIT_VALUE, 
            p.QUANTITY, 
            p.DESCRIPTION, 
            p.LOCATION, 
            p.IMAGE
        FROM PUBLISH_PRODUCT pp
        JOIN PRODUCTS p ON pp.ID_PRODUCT = p.ID_PRODUCT
        WHERE pp.ID_USER = ?
    """, (current_user["id_user"],))

    publicaciones = cursor.fetchall()
    cursor.close()

    if not publicaciones:
        raise HTTPException(status_code=404, detail="No se encontraron publicaciones para el usuario actual.")

    # Convertir las publicaciones a un formato que se ajuste al modelo PublishProduct
    resultado = []
    for pub in publicaciones:
        resultado.append(PublishProduct(
            id_publish_prod=pub[0],
            id_product=pub[1],
            id_user=pub[2],
            product_name=pub[3],
            unit_value=pub[4],
            quantity=pub[5],
            description=pub[6],
            location=pub[7],
            image=pub[8]
        ))

    return resultado


