import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="arqui_project"
    )
