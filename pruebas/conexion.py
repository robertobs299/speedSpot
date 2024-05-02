import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Laquesea123",
        database="tfg_quedadas"
    )
    return conn
