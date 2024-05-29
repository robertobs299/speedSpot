from datetime import date

import mysql.connector

from pruebas.RobertoPruebas import conexion


class Quedada:
    def __init__(self, id_quedada, nombre, descripcion, user_organiza, fecha, hora, direccion,
                 max_personas, numero_personas, active):
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

    @staticmethod
    def get_last_five(): # es mentira te las devuelve todas jijiji era bait
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Quedada order by active desc")  # Make sure this query retrieves the 'active' field
        result = cursor.fetchall()
        quedadas = []
        if result:
            for row in result:
                print(row)
                quedada = Quedada(*row)
                quedadas.append(quedada)
        return quedadas

    @staticmethod
    def get_user_asist(id_user):
        pass


    def unirse(self,id_user):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Asiste (user_id, quedada_id) VALUES (%s, %s)", (id_user, self.id_quedada))
        conn.commit()
        conn.close()




