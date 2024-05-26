from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
import pyodbc
import bcrypt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from models.user import LoginRequest
from services.db import get_db_connection
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

SECRET_KEY = 'tu_clave_secreta'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: pyodbc.Connection = Depends(get_db_connection)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no válido",
            )

        # Buscar el usuario por correo electrónico para obtener información adicional
        cursor = db.cursor()
        cursor.execute("SELECT ID_USER, IS_ADMIN FROM USERS WHERE EMAIL = ?", email)
        user_data = cursor.fetchone()
        cursor.close()

        if not user_data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        user = {
            "id_user": user_data[0],
            "email": email,
            "is_admin": user_data[1] == 1  # Convertir a booleano
        }

        return user
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido",
        )

@router.post("/login")
def login(login_data: LoginRequest, db: pyodbc.Connection = Depends(get_db_connection)):
    # Verificar las credenciales del usuario en la base de datos
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE email = ?
        """,
        (login_data.email,)
    )
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        raise HTTPException(status_code=400, detail="Correo electrónico o contraseña incorrectos")

    password_hash = result[0]

    # Verificar si la contraseña proporcionada coincide con el hash almacenado
    if not bcrypt.checkpw(login_data.password.encode('utf-8'), password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Correo electrónico o contraseña incorrectos")

    # Si la autenticación es exitosa, crear un token JWT
    access_token = create_access_token(data={"sub": login_data.email})
    return {"access_token": access_token, "token_type": "bearer"}
