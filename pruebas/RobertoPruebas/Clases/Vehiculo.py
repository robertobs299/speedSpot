class Vehiculo:
    def __init__(self, id_vehiculo, marca, modelo, anio,tipo):
        self.id_vehiculo = id_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo = tipo

    def insert(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Vehiculo (id_modelo, anio) VALUES (%s, %s)", (self.id_modelo, self.anio))
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