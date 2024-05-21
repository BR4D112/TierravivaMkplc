# database.py
import pyodbc
from fastapi import HTTPException

def get_db_connection():
    server = "localhost"  # Tu servidor
    database = "tierravivadb"  # Tu base de datos
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "PORT=1433;"
        "DATABASE=tierravivadb;"
        "UID=SA;"
        "PWD=Debian123!"  # Autenticación integrada
    )

    try:
        print(f"server{server}")
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con la base de datos: {str(e)}")
