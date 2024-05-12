from pruebas import conexion
import pandas as pd
import mysql.connector
conn = conexion.connect_to_database()
# Leer el archivo CSV
df = pd.read_csv('marcasVehiculos.csv')

cursor = conn.cursor()
# Insertar datos en la base de datos
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO Marca (id_marca, marca, tipo) VALUES (%s, %s, %s)
    ''', (row['id'], row['nombre'], row['tipo']))
    print("cargado con exito")
# Guardar los cambios y cerrar la base de datos
conn.commit()
conn.close()
