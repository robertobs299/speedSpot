from pruebas.RobertoPruebas import conexion
import pandas as pd

conn = conexion.connect_to_database()
# Leer el archivo CSV
df = pd.read_csv('modelosVehiculos.csv')

cursor = conn.cursor()
# Insertar datos en la base de datos
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO Modelo (id_marca, modelo) VALUES (%s, %s)
    ''', (row['id_marca'], row['nombre']))
    print("cargado con exito")
# Guardar los cambios y cerrar la base de datos
conn.commit()
conn.close()
