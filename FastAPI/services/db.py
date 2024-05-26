# database.py
import pyodbc
from fastapi import HTTPException

def get_db_connection():
    server = "DESKTOP-I7CE289\\SQLEXPRESS"  # Tu servidor
    database = "ss"  # Tu base de datos
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};"
        f"DATABASE={database};Trusted_Connection=yes"  # Autenticación integrada
    )

    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con la base de datos: {str(e)}")