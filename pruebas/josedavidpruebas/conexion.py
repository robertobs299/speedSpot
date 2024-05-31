import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host="speedspot-db-do-user-16519834-0.c.db.ondigitalocean.com",
        port="25060",
        user="doadmin",
        password="AVNS_DCLwHjp1kyF7kj3AsHv",
        database="Speedspot"
    )
    return conn

def get_username(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM Login WHERE id_user = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def get_user_vehicles(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    SELECT m.marca, mo.modelo, v.anio
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
def get_quedadas_organizadas(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Quedada WHERE user_organiza = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_quedadas_visitadas(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Asiste WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0
def get_best_quedada(user_id):
    conn = connect_to_database()

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

    conn.close()

    return result

def add_vehicle(user_id, marca, modelo, anio, cv, tipo):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Insertar la marca si no existe
        cursor.execute("INSERT INTO Marca (marca) VALUES (%s) ON DUPLICATE KEY UPDATE id_marca=LAST_INSERT_ID(id_marca)", (marca,))
        id_marca = cursor.lastrowid

        # Insertar el modelo si no existe
        cursor.execute("INSERT INTO Modelo (id_marca, modelo) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id_modelo=LAST_INSERT_ID(id_modelo)", (id_marca, modelo))
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
