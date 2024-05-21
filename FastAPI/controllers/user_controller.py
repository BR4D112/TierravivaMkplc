from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from models.user import UserCreate, User

import bcrypt
import pyodbc

from services.db import get_db_connection

router = APIRouter()

@router.post("/register", response_model=UserCreate)
def register_user(user_data: UserCreate, db: pyodbc.Connection = Depends(get_db_connection)):
    print("entro en este endpoint" )
    cursor = db.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), salt)

    # Insertar en PERSONS
    cursor.execute(
        """
        INSERT INTO PERSONS (FIRST_NAME, LAST_NAME, DOC_TYPE, DOC_NUMBER, PHONE_NUMBER, LOCATION)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_data.person.first_name,
            user_data.person.last_name,
            user_data.person.doc_type,
            user_data.person.doc_number,
            user_data.person.phone_number,
            user_data.person.location,
        ),
    )

    # Confirmar la inserción
    db.commit()

    # Obtener el ID del último registro
    cursor.execute("SELECT MAX(ID_PERSON) FROM PERSONS")
    row = cursor.fetchone()
    person_id = row[0]

    # Insertar en USERS
    cursor.execute(
        """
        INSERT INTO USERS (ID_PERSON, PASSWORD, EMAIL, IS_ADMIN, CREDIT_NUMBER)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            person_id,
            hashed_password,  # Usar el hash de la contraseña
            user_data.email,
            0,  # No administradores por defecto
            user_data.credit_number,  # Corregir nombre de campo
        ),
    )

    # Confirmar la inserción
    db.commit()
    print(user_data)
    return user_data


@router.get("/", response_model=List[User])
def get_users(db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT ID_USER, ID_PERSON, PASSWORD, EMAIL, CREDIT_NUMBER, IS_ADMIN FROM USERS")
    users = []
    for row in cursor.fetchall():
        user = User(
            id_user=row[0],
            id_person=row[1],
            password=row[2],
            email=row[3],
            credit_number=row[4],
            is_admin=row[5]
        )
        users.append(user)

    cursor.close()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT ID_USER, ID_PERSON, PASSWORD, EMAIL, CREDIT_NUMBER, IS_ADMIN FROM USERS WHERE ID_USER = ?", user_id)
    row = cursor.fetchone()

    if row:
        user = User(
            id_user=row[0],
            id_person=row[1],
            password=row[2],
            email=row[3],
            credit_number=row[4],
            is_admin=row[5]
        )
        cursor.close()
        return user

    cursor.close()
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/{user_id}")
def delete_user(user_id: int, db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()

    # Eliminar las referencias en PUBLISH_PRODUCT
    cursor.execute("DELETE FROM PUBLISH_PRODUCT WHERE ID_USER = ?", user_id)

    # Ahora puedes eliminar el usuario
    cursor.execute("DELETE FROM USERS WHERE ID_USER = ?", user_id)

    db.commit()
    cursor.close()
    return {"message": "Usuario eliminado exitosamente"}