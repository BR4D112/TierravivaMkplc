from http.client import HTTPException
from typing import List

import bcrypt
import pyodbc
from fastapi import APIRouter, Depends

from controllers.auth_controller import get_current_user
from models.user import UserCreate, User, UserInfo
from services.db import get_db_connection

router = APIRouter()

@router.post("/register", response_model=UserCreate)
def register_user(user_data: UserCreate, db: pyodbc.Connection = Depends(get_db_connection)):
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



@router.get("/users/me/", response_model=UserInfo)
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


@router.get("/me", response_model=User)
def get_me(current_user: dict = Depends(get_current_user), db: pyodbc.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT ID_USER, ID_PERSON, PASSWORD, EMAIL, CREDIT_NUMBER, IS_ADMIN 
        FROM USERS 
        WHERE ID_USER = ?
        """,
        current_user["id_user"]
    )
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