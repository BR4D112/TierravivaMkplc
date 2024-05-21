from http.client import HTTPException

from fastapi import APIRouter, Depends
from models.product import ProductCreate, ProductUpdate, Product
from typing import List
import pyodbc
from controllers.auth_controller import get_current_user
from services.db import get_db_connection

router = APIRouter()
#   Crear  producto


@router.get("/", response_model=List[Product])
def get_products(db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            ID_PRODUCT,
            ID_CATEGORIE,
            ID_MEASURE_PROD,
            PRODUCT_NAME,
            UNIT_VALUE,
            QUANTITY,
            DESCRIPTION,
            LOCATION,
            IMAGE
        FROM PRODUCTS
    """)
    products = [
        Product(
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
        for row in cursor.fetchall()
    ]
    cursor.close()
    return products

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