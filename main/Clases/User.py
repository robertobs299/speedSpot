
from pruebas.RobertoPruebas import conexion


class User:
    def __init__(self, email, name, surname, cp, phone, id):
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

    def validate_user(self,username,password):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id_user FROM Login WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            conn = conexion.connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT id_user,cp,email,telefono,nombre,apellidos FROM User WHERE id_user = %s", (result[0],))
            result = cursor.fetchone()
            conn.close()
            self.id, self.cp, self.email, self.phone, self.name, self.surname = result
            return User(self.email, self.name, self.surname, self.cp, self.phone, self.id)
        else:
            self.email, self.name, self.surname, self.cp, self.phone = None, None, None, None, None
            return None

    def insert_user(self,username,password):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (email, nombre, apellidos, cp, telefono) VALUES (%s, %s, %s, %s, %s)", (self.email, self.name, self.surname, self.cp, self.phone))
        cursor.execute("insert into Login (username, password, id_user) values (%s, %s, %s)", (username, password, cursor.lastrowid))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def update_user(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET email = %s, nombre = %s, apellidos = %s, cp = %s, telefono = %s WHERE id_user = %s", (self.email, self.name, self.surname, self.cp, self.phone, self.id))
        conn.commit()
        conn.close()

    def exist_user(username):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id_user FROM Login WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        if not result:
            return False
        return True

