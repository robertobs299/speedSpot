import mysql

from main.Clases import conexion


class Vehiculo:
    def __init__(self, id_vehiculo, marca, modelo, anio,tipo):
        self.id_vehiculo = id_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo = tipo

    def insert(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Vehiculo (id_modelo, anio) VALUES (%s, %s)", (self.modelo, self.anio))
        self.id_vehiculo = cursor.lastrowid
        conn.commit()

    @staticmethod
    def get_by_id(conn, id_vehiculo):
        cursor = conn.cursor()
        cursor.execute("SELECT id_vehiculo, ma.marca,m.modelo,v.anio, tipo FROM Vehiculo v join Modelo m on v.id_modelo = m.modelo join Marca ma on m.id_marca = ma.id_marca WHERE id_vehiculo = %s", (id_vehiculo,))
        result = cursor.fetchone()
        if result:
            vehiculo = Vehiculo(id_vehiculo=result[0], marca=result[1], modelo=result[2], anio=result[3], tipo=result[4])
            return vehiculo
        else:
            return None


    @staticmethod
    def get_user_vehicles(user_id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        query = """
        SELECT m.marca, mo.modelo, v.anio, v.cv
        FROM Vehiculo v
        JOIN Modelo mo ON v.id_modelo = mo.id_modelo
        JOIN Marca m ON mo.id_marca = m.id_marca
        JOIN Tiene t ON v.id_vehiculo = t.id_vehiculo
        WHERE t.id_user = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def add_vehicle(user_id, marca, modelo, anio, cv):
        try:
            connection = conexion.connect_to_database()
            cursor = connection.cursor()

            # Insertar la marca si no existe
            cursor.execute(
                "INSERT INTO Marca (marca) VALUES (%s) ON DUPLICATE KEY UPDATE id_marca=LAST_INSERT_ID(id_marca)",
                (marca,))
            id_marca = cursor.lastrowid

            # Insertar el modelo si no existe
            cursor.execute(
                "INSERT INTO Modelo (id_marca, modelo) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id_modelo=LAST_INSERT_ID(id_modelo)",
                (id_marca, modelo))
            id_modelo = cursor.lastrowid

            # Insertar el vehículo
            cursor.execute("INSERT INTO Vehiculo (id_modelo, anio) VALUES (%s, %s)", (id_modelo, anio))
            id_vehiculo = cursor.lastrowid

            # Relacionar el vehículo con el usuario
            cursor.execute("INSERT INTO Tiene (id_user, id_vehiculo) VALUES (%s, %s)", (user_id, id_vehiculo))

            connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to add vehicle: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_marca_options():
        try:
            # Conexión a la base de datos
            conn = conexion.connect_to_database()
            cursor = conn.cursor()
            query = "SELECT marca FROM Marca"
            cursor.execute(query)
            marcas = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            return marcas

        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)
            return []