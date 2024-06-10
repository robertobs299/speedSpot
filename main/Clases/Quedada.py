from datetime import date

import mysql.connector

from pruebas.RobertoPruebas import conexion

#Clase que contiene la información de una quedada en la base de datos y una serie de métodos para interactuar con ella
class Quedada:
    def __init__(self, id_quedada, nombre, descripcion, user_organiza, fecha, hora, direccion,
                 max_personas, numero_personas, active, imagen):
        self.id_quedada = id_quedada
        self.nombre = nombre
        self.descripcion = descripcion
        self.user_organiza = user_organiza
        self.fecha = fecha
        self.hora = hora
        self.direccion = direccion
        self.max_personas = max_personas
        self.numero_personas = numero_personas
        self.active = active
        self.imagen = imagen


    @staticmethod
    def recuperar_quedadas(filtros=None):
        conn = conexion.connect_to_database()

        cursor = conn.cursor()

        query = "SELECT * FROM Quedada"
        condiciones = []
        valores = []

        if filtros:
            if 'nombre' in filtros:
                condiciones.append("nombre = %s")
                valores.append(filtros['nombre'])
            if 'fecha' in filtros:
                condiciones.append("fecha = %s")
                valores.append(filtros['fecha'])
            if 'numero_personas' in filtros:
                condiciones.append("numero_personas = %s")
                valores.append(filtros['numero_personas'])
            if 'max_personas' in filtros:
                condiciones.append("max_personas = %s")
                valores.append(filtros['max_personas'])

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        query += "LIMIT 50"

        cursor.execute(query, valores)

        quedadas = []

        for (id_quedada, nombre, descripcion, user_organiza, fecha, hora, direccion, max_personas,
             numero_personas) in cursor:
            quedada = Quedada(
                id_quedada=id_quedada,
                nombre=nombre,
                descripcion=descripcion,
                user_organiza=user_organiza,
                fecha=fecha,
                hora=hora,
                direccion=direccion,
                max_personas=max_personas,
                numero_personas=numero_personas
            )
            quedadas.append(quedada)

        cursor.close()
        conn.close()

        return quedadas
#Método que inserta una quedada en la base de datos
    def insertar_quedada(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Quedada (nombre, descripcion, user_organiza, fecha, hora, direccion, max_personas, numero_personas, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)",
            (self.nombre, self.descripcion, self.user_organiza, self.fecha, self.hora, self.direccion,
             self.max_personas, self.numero_personas,self.active))
        self.id_quedada = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id_quedada

    @staticmethod
    def get_last_five(): # es mentira te las devuelve todas jijiji era bait
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Quedada where active = 1 order by fecha desc")  # Make sure this query retrieves the 'active' field
        result = cursor.fetchall()
        quedadas = []
        if result:
            for row in result:
                print(row)
                quedada = Quedada(*row)
                quedadas.append(quedada)
        return quedadas
#Metodo que devuelve la lista de quedadas a las que un usuario ha asistido
    @staticmethod
    def get_quedadas_user_asist(id_user):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT q.* FROM Asiste a join Quedada q on a.quedada_id = q.id_quedada where a.user_id = %s", (id_user,))
        result = cursor.fetchall()
        quedadas = []
        if result:
            for row in result:
                quedada = Quedada(*row)
                quedadas.append(quedada)
        return quedadas
#Metodo que permite al usuario unirse a una quedada
    @staticmethod
    def unirse(id_user,id_quedada):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Asiste (user_id, quedada_id) VALUES (%s, %s)", (id_user,id_quedada))
        cursor.execute("UPDATE Quedada SET numero_personas = numero_personas + 1 WHERE id_quedada = %s", (id_quedada,))
        conn.commit()
        conn.close()
    @staticmethod
    def desapuntarse(id_user,id_quedada):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Asiste WHERE user_id = %s AND quedada_id = %s", (id_user, id_quedada))
        cursor.execute("UPDATE Quedada SET numero_personas = numero_personas - 1 WHERE id_quedada = %s", (id_quedada,))
        conn.commit()
        conn.close()
#Metodo que actualiza las fotos que tiene una quedada
    @staticmethod
    def updateFotoQuedada(id_quedada, ruta_imagen):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE Quedada SET image = %s WHERE id_quedada = %s", (ruta_imagen, id_quedada))
        conn.commit()
        conn.close()

    @staticmethod
    def get_quedadas_organizadas(user_id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Quedada WHERE user_organiza = %s", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    @staticmethod
    def get_quedadas_visitadas(user_id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Asiste WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    @staticmethod
    def get_best_quedada(user_id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()

        query = """
        SELECT q.id_quedada, q.nombre, q.fecha, q.numero_personas, f.enlace_foto, d.direccion, p.localidad
        FROM Quedada q
        JOIN Fotos_quedada f ON q.id_quedada = f.quedada_id
        JOIN Direccion d ON q.direccion = d.id_direccion
        JOIN Postal_code p ON d.cp = p.id_cp
        WHERE q.user_organiza = %s
        ORDER BY q.numero_personas DESC
        LIMIT 1
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        query2 = """
            SELECT q.id_quedada, q.nombre, q.fecha, q.numero_personas, f.enlace_foto, d.direccion, p.localidad
            FROM Quedada q
            JOIN Fotos_quedada f ON q.id_quedada = f.quedada_id
            JOIN Direccion d ON q.direccion = d.id_direccion
            JOIN Postal_code p ON d.cp = p.id_cp
            ORDER BY q.numero_personas DESC
            LIMIT 1
        """
        cursor.execute(query2)
        result2 = cursor.fetchone()

        conn.close()

        return result if result else result2

#Clase que contiene informacion extra de otras tablas
class Quedada2:
    def __init__(self, id_quedada, nombre, descripcion, user_organiza, fecha, hora, cp, tipo_via, direccion, max_personas, numero_personas, organizador_nombre, organizador_apellidos):
        self.id_quedada = id_quedada
        self.nombre = nombre
        self.descripcion = descripcion
        self.user_organiza = user_organiza
        self.fecha = fecha
        self.hora = hora
        self.cp = cp
        self.tipo_via = tipo_via
        self.direccion = direccion
        self.max_personas = max_personas
        self.numero_personas = numero_personas
        self.organizador_nombre = organizador_nombre
        self.organizador_apellidos = organizador_apellidos

    @staticmethod
    def get_last_five():
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT q.id_quedada, q.nombre, q.descripcion, q.user_organiza, q.fecha, q.hora, d.cp, d.tipo_via, d.direccion, q.max_personas, q.numero_personas, u.nombre, u.apellidos
            FROM Quedada q
            JOIN User u ON q.user_organiza = u.id_user
            JOIN Direccion d ON q.direccion = d.id_direccion
            ORDER BY q.fecha DESC
            LIMIT 5
        """)
        quedadas = []
        for row in cursor.fetchall():
            quedada = Quedada2(
                id_quedada=row[0],
                nombre=row[1],
                descripcion=row[2],
                user_organiza=row[3],
                fecha=row[4],
                hora=row[5],
                cp=row[6],
                tipo_via=row[7],
                direccion=row[8],
                max_personas=row[9],
                numero_personas=row[10],
                organizador_nombre=row[11],
                organizador_apellidos=row[12]
            )
            quedadas.append(quedada)
        cursor.close()
        conn.close()
        return quedadas

    @staticmethod
    def unirse(id_user, id_quedada):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Asiste (user_id, quedada_id) VALUES (%s, %s)", (id_user, id_quedada))
        cursor.execute("UPDATE Quedada SET numero_personas = numero_personas + 1 WHERE id_quedada = %s", (id_quedada,))
        conn.commit()
        conn.close()

    @staticmethod
    def desapuntarse(id_user, id_quedada):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Asiste WHERE user_id = %s AND quedada_id = %s", (id_user, id_quedada))
        cursor.execute("UPDATE Quedada SET numero_personas = numero_personas - 1 WHERE id_quedada = %s", (id_quedada,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT q.id_quedada, q.nombre, q.descripcion, q.user_organiza, q.fecha, q.hora, d.cp, d.tipo_via, d.direccion, q.max_personas, q.numero_personas, u.nombre, u.apellidos
            FROM Quedada q
            JOIN User u ON q.user_organiza = u.id_user
            JOIN Direccion d ON q.direccion = d.id_direccion
            WHERE q.id_quedada = %s
        """, (id,))

        row = cursor.fetchone()
        if row is not None:
            quedada = Quedada2(
                id_quedada=row[0],
                nombre=row[1],
                descripcion=row[2],
                user_organiza=row[3],
                fecha=row[4],
                hora=row[5],
                cp=row[6],
                tipo_via=row[7],
                direccion=row[8],
                max_personas=row[9],
                numero_personas=row[10],
                organizador_nombre=row[11],
                organizador_apellidos=row[12]
            )
        else:
            quedada = None
        cursor.close()
        conn.close()
        return quedada