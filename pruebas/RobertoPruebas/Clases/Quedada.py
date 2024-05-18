from datetime import date

import mysql.connector

from pruebas.RobertoPruebas import conexion


class Quedada:
    def __init__(self, id_quedada, nombre, descripcion, user_organiza, fecha, hora, coordenadas, direccion_fin,
                 max_personas, numero_personas):
        self.id_quedada = id_quedada
        self.nombre = nombre
        self.descripcion = descripcion
        self.user_organiza = user_organiza
        self.fecha = fecha
        self.hora = hora
        self.coordenadas = coordenadas
        self.direccion_fin = direccion_fin
        self.max_personas = max_personas
        self.numero_personas = numero_personas

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
            if 'coordenadas' in filtros:
                condiciones.append("coordenadas = %s")
                valores.append(filtros['coordenadas'])

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        query += "LIMIT 10"

        cursor.execute(query, valores)

        quedadas = []

        for (id_quedada, nombre, descripcion, user_organiza, fecha, hora, coordenadas, direccion_fin, max_personas,
             numero_personas) in cursor:
            quedada = Quedada(
                id_quedada=id_quedada,
                nombre=nombre,
                descripcion=descripcion,
                user_organiza=user_organiza,
                fecha=fecha,
                hora=hora,
                coordenadas=coordenadas,
                direccion_fin=direccion_fin,
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
            "INSERT INTO Quedada (nombre, descripcion, user_organiza, fecha, hora, coordenadas, direccion_fin, max_personas, numero_personas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self.nombre, self.descripcion, self.user_organiza, self.fecha, self.hora, self.coordenadas,
             self.direccion_fin, self.max_personas, self.numero_personas))
        self.id_quedada = cursor.lastrowid
        conn.commit()
        conn.close()



# Ejemplo de uso con filtros
filtros = {
    'nombre': 'Reunión de Desarrollo',
    'fecha': date(2024, 5, 20),
    'numero_personas': 10
}

