import hashlib

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from pruebas import conexion


class registroScreen(BoxLayout):
    def registrar(self,email, password, username,name, surname, postalcode, phone, sexo,):
        # if email == '' or password == '' or username == '' or name == '' or surname == '' or postalcode == '' or phone == '' or sexo == '':
        #     return False
        # if len(password) < 8:
        #     return False
        # if len(phone) != 9:
        #     return False
        # if len(postalcode) != 5:
        #     return False
        # la idea es recoger los errores y mostrarlos en un popup
        if sexo == "Hombre":
            sexo = "H"
        else:
            sexo = "M"

        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # Conexión a la base de datos
        conn = conexion.connect_to_database()
        cursor = conn.cursor()

        # Buscar el ID del código postal
        cursor.execute("SELECT id_cp FROM postal_code WHERE cp LIKE %s", (str(postalcode),))
        result = cursor.fetchone()  # Obtener el resultado de la consulta

        if result:
            idCp = result[0]  # Obtener el ID del código postal
        else:
            # Si no se encuentra el código postal, puedes manejar el error aquí
            print("El código postal no existe en la base de datos")
            conn.close()
            print(result)

        # Calcular el hash de la contraseña
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # Insertar el usuario en la tabla User
        cursor.execute(
            "INSERT INTO User (email, nombre, apellidos, cp, telefono, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
            (email, name, surname, idCp, phone, sexo))

        iduser = cursor.lastrowid

        # Insertar los datos de inicio de sesión en la tabla Login
        cursor.execute("INSERT INTO Login (id_user, username, password) VALUES (%s, %s, %s)",
                       (iduser, username, encrypted_password))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()



class MyApp(App):
    pass

MyApp().run()

