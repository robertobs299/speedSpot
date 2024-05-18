import mysql.connector

from pruebas.RobertoPruebas import conexion


class User:
    def __init__(self, email, name, surname, cp, phone,id):
        self.email = email
        self.name = name
        self.surname = surname
        self.cp = cp
        self.phone = phone
        self.id = id

    def get_user(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id_user,cp,email,telefono,nombre,apellidos FROM User WHERE id_user = %s", (self.id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.id, self.cp, self.email, self.phone, self.name, self.surname = result
            return User(self.email, self.name, self.surname, self.cp, self.phone, self.id)
        else:
            self.email, self.name, self.surname, self.cp, self.phone = None, None, None, None, None
            return None

    def insert_user(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (email, nombre, apellidos, cp, telefono) VALUES (%s, %s, %s, %s, %s)", (self.email, self.name, self.surname, self.cp, self.phone))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def update_user(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET email = %s, nombre = %s, apellidos = %s, cp = %s, telefono = %s WHERE id_user = %s", (self.email, self.name, self.surname, self.cp, self.phone, self.id))
        conn.commit()
        conn.close()

