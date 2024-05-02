from pruebas import conexion
import pandas as pd
import mysql.connector
conn = conexion.connect_to_database()
# Leer el archivo CSV
df = pd.read_csv('modelosVehiculos.csv')

cursor = conn.cursor()
# Insertar datos en la base de datos
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO modelo (id_marca, modelo) VALUES (%s, %s)
    ''', (row['id_marca'], row['nombre']))

# Guardar los cambios y cerrar la base de datos
conn.commit()
conn.close()
